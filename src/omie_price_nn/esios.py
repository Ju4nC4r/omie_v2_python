from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import requests


ESIOS_API_URL = "https://api.esios.ree.es/indicators/{indicator_id}"
ESIOS_GENERATION_COLUMNS = [
    "wind_forecast_mwh",
    "solar_pv_forecast_mwh",
    "solar_thermal_forecast_mwh",
    "renewable_forecast_mwh",
    "solar_forecast_mwh",
    "wind_solar_ratio",
]
ESIOS_FORECAST_INDICATORS = {
    "wind_forecast_mwh": 541,
    "solar_pv_forecast_mwh": 542,
    "solar_thermal_forecast_mwh": 543,
}


def _headers(token: str) -> dict[str, str]:
    return {
        "Accept": "application/json; application/vnd.esios-api-v1+json",
        "Content-Type": "application/json",
        "x-api-key": token,
    }


def _normalize_timestamp(values: pd.Series) -> pd.Series:
    return pd.to_datetime(values, utc=True).dt.tz_convert("Europe/Madrid").dt.tz_localize(None)


def download_esios_indicator(indicator_id: int, start: date, end: date, token: str) -> pd.DataFrame:
    response = requests.get(
        ESIOS_API_URL.format(indicator_id=indicator_id),
        headers=_headers(token),
        params={
            "start_date": f"{start.isoformat()}T00:00:00",
            "end_date": f"{end.isoformat()}T23:59:59",
            "time_trunc": "hour",
        },
        timeout=45,
    )
    response.raise_for_status()
    values = response.json()["indicator"]["values"]
    if not values:
        return pd.DataFrame(columns=["timestamp", "value"])

    data = pd.DataFrame(values)
    data["timestamp"] = _normalize_timestamp(data["datetime"])
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    return data.groupby("timestamp", as_index=False)["value"].sum()


def load_esios_generation(start: date, end: date, token: str, cache_dir: Path = Path("data/processed")) -> pd.DataFrame:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"esios_generation_{start:%Y%m%d}_{end:%Y%m%d}.csv"
    if cache_path.exists() and cache_path.stat().st_size > 0:
        return pd.read_csv(cache_path, parse_dates=["timestamp"])

    frames = []
    for column, indicator_id in ESIOS_FORECAST_INDICATORS.items():
        frame = download_esios_indicator(indicator_id, start, end, token)
        frame = frame.rename(columns={"value": column})
        frames.append(frame)

    generation = frames[0]
    for frame in frames[1:]:
        generation = generation.merge(frame, on="timestamp", how="outer")

    generation = generation.sort_values("timestamp").reset_index(drop=True)
    generation["solar_forecast_mwh"] = (
        generation["solar_pv_forecast_mwh"].fillna(0) + generation["solar_thermal_forecast_mwh"].fillna(0)
    )
    generation["renewable_forecast_mwh"] = generation["wind_forecast_mwh"].fillna(0) + generation[
        "solar_forecast_mwh"
    ].fillna(0)
    generation["wind_solar_ratio"] = generation["wind_forecast_mwh"] / generation["solar_forecast_mwh"].replace(
        0, pd.NA
    )
    generation.to_csv(cache_path, index=False)
    return generation


def enrich_with_esios_generation(data: pd.DataFrame, start: date, end: date, token: str) -> pd.DataFrame:
    generation = load_esios_generation(start, end, token)
    if generation.empty:
        raise ValueError("ESIOS returned no generation forecast values for the selected date range.")

    enriched = data.copy()
    enriched["timestamp"] = pd.to_datetime(enriched["timestamp"])
    enriched = enriched.sort_values("timestamp").reset_index(drop=True)
    generation = generation.sort_values("timestamp").reset_index(drop=True)

    enriched = pd.merge_asof(
        enriched,
        generation,
        on="timestamp",
        direction="backward",
        tolerance=pd.Timedelta(hours=1),
    )
    enriched[ESIOS_GENERATION_COLUMNS] = enriched[ESIOS_GENERATION_COLUMNS].ffill().bfill()
    return enriched
