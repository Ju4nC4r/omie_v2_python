from __future__ import annotations

import argparse
from pathlib import Path

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
    data = pd.read_csv(Path(args.data_path))
    x_next, next_timestamp = make_next_prediction_features(data)
    prediction = model.predict(x_next)[0]

    print(f"Prediccion para {next_timestamp}: {prediction:.2f} EUR/MWh")


if __name__ == "__main__":
    main()
