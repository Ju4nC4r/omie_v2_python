from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Callable

os.environ.setdefault("MPLCONFIGDIR", str(Path("data/.matplotlib").resolve()))
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

import joblib
import matplotlib
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import RidgeCV
from sklearn.metrics import mean_absolute_error, r2_score

matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from sklearn.metrics import root_mean_squared_error
except ImportError:  # scikit-learn < 1.4
    from sklearn.metrics import mean_squared_error

    def root_mean_squared_error(y_true, y_pred):
        return mean_squared_error(y_true, y_pred, squared=False)
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.compose import TransformedTargetRegressor
from sklearn.preprocessing import RobustScaler, StandardScaler

from .data import OmieConfig, load_omie_prices, parse_date
from .features import make_supervised_dataset


ProgressCallback = Callable[[str], None]
MODEL_CHOICES = ("auto", "ridge", "mlp", "hist_gradient_boosting")


def build_model_candidates():
    return {
        "ridge": make_pipeline(
            RobustScaler(),
            TransformedTargetRegressor(
                regressor=RidgeCV(alphas=[0.1, 1.0, 10.0, 100.0]),
                transformer=StandardScaler(),
            ),
        ),
        "mlp": make_pipeline(
            StandardScaler(),
            TransformedTargetRegressor(
                regressor=MLPRegressor(
                    hidden_layer_sizes=(64, 32),
                    activation="relu",
                    solver="adam",
                    alpha=0.01,
                    batch_size=64,
                    learning_rate="adaptive",
                    learning_rate_init=0.0003,
                    max_iter=1500,
                    early_stopping=True,
                    validation_fraction=0.2,
                    n_iter_no_change=50,
                    random_state=42,
                ),
                transformer=StandardScaler(),
            ),
        ),
        "hist_gradient_boosting": HistGradientBoostingRegressor(
            loss="absolute_error",
            max_iter=400,
            learning_rate=0.04,
            max_leaf_nodes=15,
            l2_regularization=0.1,
            random_state=42,
        ),
    }


def train_model(
    data: pd.DataFrame,
    model_path: Path,
    plot_path: Path,
    model_choice: str = "auto",
    progress_callback: ProgressCallback | None = None,
):
    def report(message: str) -> None:
        if progress_callback:
            progress_callback(message)

    report("Construyendo dataset supervisado...")
    if model_choice not in MODEL_CHOICES:
        raise ValueError(f"Unknown model choice {model_choice!r}. Valid choices: {', '.join(MODEL_CHOICES)}")

    x, y = make_supervised_dataset(data)
    if len(x) < 700:
        raise ValueError("Not enough rows after feature creation. Use a wider date range.")

    split_at = int(len(x) * 0.8)
    x_train, x_test = x.iloc[:split_at], x.iloc[split_at:]
    y_train, y_test = y.iloc[:split_at], y.iloc[split_at:]

    candidates = build_model_candidates()
    if model_choice != "auto":
        candidates = {model_choice: candidates[model_choice]}

    candidate_metrics = {}
    best_name = ""
    best_model = None
    best_predictions = None
    best_mae = float("inf")

    for name, candidate in candidates.items():
        report(f"Entrenando candidato: {name}...")
        candidate.fit(x_train, y_train)
        report(f"Evaluando candidato: {name}...")
        candidate_predictions = candidate.predict(x_test)
        candidate_mae = mean_absolute_error(y_test, candidate_predictions)
        candidate_metrics[name] = {
            "mae": candidate_mae,
            "rmse": root_mean_squared_error(y_test, candidate_predictions),
            "r2": r2_score(y_test, candidate_predictions),
        }
        if model_choice == name or candidate_mae < best_mae:
            best_name = name
            best_model = candidate
            best_predictions = candidate_predictions
            best_mae = candidate_mae
        report(f"Candidato {name} completado: MAE {candidate_mae:.2f} EUR/MWh")

    if best_model is None or best_predictions is None:
        raise RuntimeError("No model candidate could be trained.")

    report(f"Mejor candidato: {best_name}. Guardando modelo y grafica...")
    predictions = best_predictions
    baseline = x_test["price_lag_24"].to_numpy()
    metrics = {
        "best_model": best_name,
        "model_choice": model_choice,
        "mae": mean_absolute_error(y_test, predictions),
        "rmse": root_mean_squared_error(y_test, predictions),
        "r2": r2_score(y_test, predictions),
        "baseline_lag_24_mae": mean_absolute_error(y_test, baseline),
        "baseline_lag_24_rmse": root_mean_squared_error(y_test, baseline),
        "train_rows": len(x_train),
        "test_rows": len(x_test),
        "feature_count": len(x.columns),
        "candidates": candidate_metrics,
    }

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": best_model, "feature_columns": list(x.columns), "metrics": metrics}, model_path)

    plot_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(12, 5))
    plt.plot(y_test.to_numpy()[:240], label="real")
    plt.plot(predictions[:240], label=f"modelo {best_name}")
    plt.plot(baseline[:240], label="baseline lag 24", alpha=0.65)
    plt.title("Validacion OMIE: precio marginal espanol")
    plt.ylabel("EUR/MWh")
    plt.xlabel("periodos del tramo de validacion")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path, dpi=140)
    plt.close()

    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Entrena y selecciona un modelo para precio OMIE Espana.")
    parser.add_argument("--start", required=True, help="Fecha inicial YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="Fecha final YYYY-MM-DD")
    parser.add_argument("--model-path", default="models/omie_model.joblib")
    parser.add_argument("--plot-path", default="models/validation_plot.png")
    parser.add_argument(
        "--model",
        choices=MODEL_CHOICES,
        default="auto",
        help="Modelo a entrenar. auto prueba todos y guarda el de menor MAE.",
    )
    args = parser.parse_args()

    data = load_omie_prices(parse_date(args.start), parse_date(args.end), OmieConfig())
    metrics = train_model(data, Path(args.model_path), Path(args.plot_path), model_choice=args.model)

    print("Entrenamiento completado")
    print(f"Seleccion solicitada: {metrics['model_choice']}")
    print(f"Mejor modelo: {metrics['best_model']}")
    print(f"MAE: {metrics['mae']:.2f} EUR/MWh")
    print(f"RMSE: {metrics['rmse']:.2f} EUR/MWh")
    print(f"R2: {metrics['r2']:.3f}")
    print(f"Baseline lag 24 MAE: {metrics['baseline_lag_24_mae']:.2f} EUR/MWh")
    for name, values in metrics["candidates"].items():
        print(f"Candidato {name}: MAE {values['mae']:.2f}, RMSE {values['rmse']:.2f}, R2 {values['r2']:.3f}")
    print(f"Variables usadas: {metrics['feature_count']}")
    print(f"Filas entrenamiento: {metrics['train_rows']}")
    print(f"Filas validacion: {metrics['test_rows']}")


if __name__ == "__main__":
    main()
