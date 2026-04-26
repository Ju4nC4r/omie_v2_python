from __future__ import annotations

import numpy as np
import pandas as pd


TARGET_COLUMN = "marginal_es"
EXTERNAL_FEATURE_COLUMNS = [
    "wind_forecast_mwh",
    "solar_pv_forecast_mwh",
    "solar_thermal_forecast_mwh",
    "renewable_forecast_mwh",
    "solar_forecast_mwh",
    "wind_solar_ratio",
]
LAGS = (1, 2, 3, 4, 5, 6, 12, 23, 24, 25, 48, 72, 168, 336)
ROLLING_WINDOWS = (3, 6, 12, 24, 48, 168)
BASE_FEATURE_COLUMNS = [
    "period",
    "time_of_day_sin",
    "time_of_day_cos",
    "hour_sin",
    "hour_cos",
    "dow_sin",
    "dow_cos",
    "month_sin",
    "month_cos",
    "is_weekend",
    *[f"price_lag_{lag}" for lag in LAGS],
    *[f"price_roll_{window}_mean" for window in ROLLING_WINDOWS],
    *[f"price_roll_{window}_std" for window in ROLLING_WINDOWS],
    "price_roll_24_min",
    "price_roll_24_max",
    "price_roll_168_min",
    "price_roll_168_max",
    "price_diff_1",
    "price_diff_24",
    "price_diff_168",
    "price_ratio_24",
    "price_ratio_168",
]
FEATURE_COLUMNS = BASE_FEATURE_COLUMNS


def get_feature_columns(data: pd.DataFrame) -> list[str]:
    external = [column for column in EXTERNAL_FEATURE_COLUMNS if column in data.columns]
    return [*BASE_FEATURE_COLUMNS, *external]


def add_time_features(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    hour = df["timestamp"].dt.hour
    minute = df["timestamp"].dt.minute
    dayofweek = df["timestamp"].dt.dayofweek
    month = df["timestamp"].dt.month
    minute_of_day = hour * 60 + minute

    df["time_of_day_sin"] = np.sin(2 * np.pi * minute_of_day / 1440)
    df["time_of_day_cos"] = np.cos(2 * np.pi * minute_of_day / 1440)
    df["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    df["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    df["dow_sin"] = np.sin(2 * np.pi * dayofweek / 7)
    df["dow_cos"] = np.cos(2 * np.pi * dayofweek / 7)
    df["month_sin"] = np.sin(2 * np.pi * month / 12)
    df["month_cos"] = np.cos(2 * np.pi * month / 12)
    df["is_weekend"] = (dayofweek >= 5).astype(int)
    return df


def build_feature_frame(data: pd.DataFrame) -> pd.DataFrame:
    df = add_time_features(data)
    shifted_price = df[TARGET_COLUMN].shift(1)

    for lag in LAGS:
        df[f"price_lag_{lag}"] = df[TARGET_COLUMN].shift(lag)

    for window in ROLLING_WINDOWS:
        rolling = shifted_price.rolling(window)
        df[f"price_roll_{window}_mean"] = rolling.mean()
        df[f"price_roll_{window}_std"] = rolling.std()

    df["price_roll_24_min"] = shifted_price.rolling(24).min()
    df["price_roll_24_max"] = shifted_price.rolling(24).max()
    df["price_roll_168_min"] = shifted_price.rolling(168).min()
    df["price_roll_168_max"] = shifted_price.rolling(168).max()
    df["price_diff_1"] = df["price_lag_1"] - df["price_lag_2"]
    df["price_diff_24"] = df["price_lag_1"] - df["price_lag_24"]
    df["price_diff_168"] = df["price_lag_1"] - df["price_lag_168"]
    df["price_ratio_24"] = df["price_lag_1"] / df["price_lag_24"].replace(0, np.nan)
    df["price_ratio_168"] = df["price_lag_1"] / df["price_lag_168"].replace(0, np.nan)
    return df


def make_supervised_dataset(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    df = build_feature_frame(data)
    feature_columns = get_feature_columns(df)
    df = df.dropna(subset=feature_columns + [TARGET_COLUMN]).reset_index(drop=True)
    return df[feature_columns], df[TARGET_COLUMN]


def make_next_prediction_features(
    data: pd.DataFrame, expected_feature_columns: list[str] | None = None
) -> tuple[pd.DataFrame, pd.Timestamp]:
    df = data.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    recent_deltas = df["timestamp"].diff().dropna()
    step = recent_deltas.mode().iloc[0] if not recent_deltas.empty else pd.Timedelta(hours=1)
    next_timestamp = df["timestamp"].iloc[-1] + step

    same_day = df[df["timestamp"].dt.date == next_timestamp.date()]
    next_period = int(same_day["period"].max() + 1) if not same_day.empty else 1
    next_row = {
        "date": next_timestamp.date(),
        "period": next_period,
        "timestamp": next_timestamp,
        "marginal_pt": np.nan,
        TARGET_COLUMN: np.nan,
    }
    expected_feature_columns = expected_feature_columns or get_feature_columns(df)
    for column in EXTERNAL_FEATURE_COLUMNS:
        if column in expected_feature_columns and column in df.columns:
            next_row[column] = df[column].ffill().iloc[-1]

    future = pd.concat([df, pd.DataFrame([next_row])], ignore_index=True)
    featured = build_feature_frame(future)
    x_next = featured.tail(1)[expected_feature_columns]
    if x_next.isna().any(axis=None):
        raise ValueError("Not enough history to build prediction features for the next period.")
    return x_next, next_timestamp
