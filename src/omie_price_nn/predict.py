from __future__ import annotations

import argparse
import os
from pathlib import Path

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

import joblib
import pandas as pd

from .features import make_next_prediction_features


def main() -> None:
    parser = argparse.ArgumentParser(description="Predice la siguiente hora usando el modelo entrenado.")
    parser.add_argument("--model-path", default="models/omie_model.joblib")
    parser.add_argument("--data-path", default="data/processed/omie_prices.csv")
    args = parser.parse_args()

    bundle = joblib.load(args.model_path)
    model = bundle["model"]
    feature_columns = bundle.get("feature_columns")
    data = pd.read_csv(Path(args.data_path))
    x_next, next_timestamp = make_next_prediction_features(data, expected_feature_columns=feature_columns)
    prediction = model.predict(x_next)[0]

    print(f"Prediccion para {next_timestamp}: {prediction:.2f} EUR/MWh")


if __name__ == "__main__":
    main()
