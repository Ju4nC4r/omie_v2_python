from __future__ import annotations

import queue
import threading
import traceback
import webbrowser
from pathlib import Path
from tkinter import END, LEFT, BOTH, StringVar, Tk, Text
from tkinter import messagebox
from tkinter import ttk

import joblib
import pandas as pd

from .data import OmieConfig, load_omie_prices, parse_date
from .features import make_next_prediction_features, make_supervised_dataset
from .train import train_model


DATA_PATH = Path("data/processed/omie_prices.csv")
FEATURES_PATH = Path("data/processed/omie_features.csv")
MODEL_PATH = Path("models/omie_model.joblib")
PLOT_PATH = Path("models/validation_plot.png")


class OmiePriceApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("OMIE Price Model")
        self.root.geometry("980x680")
        self.events: queue.Queue[tuple[str, object]] = queue.Queue()
        self.is_running = False

        self.start_var = StringVar(value="2025-01-01")
        self.end_var = StringVar(value="2025-03-31")
        self.status_var = StringVar(value="Listo")
        self.data_var = StringVar(value="-")
        self.features_var = StringVar(value="-")
        self.model_var = StringVar(value="-")
        self.prediction_var = StringVar(value="-")

        self._build_ui()
        self.root.after(150, self._poll_events)

    def _build_ui(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(3, weight=1)

        header = ttk.Frame(self.root, padding=14)
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(5, weight=1)

        ttk.Label(header, text="Fecha inicio").grid(row=0, column=0, sticky="w")
        ttk.Entry(header, width=14, textvariable=self.start_var).grid(row=0, column=1, padx=(6, 18))
        ttk.Label(header, text="Fecha fin").grid(row=0, column=2, sticky="w")
        ttk.Entry(header, width=14, textvariable=self.end_var).grid(row=0, column=3, padx=(6, 18))
        ttk.Button(header, text="Ejecutar todo", command=self.run_all).grid(row=0, column=4, padx=(0, 8))
        ttk.Label(header, textvariable=self.status_var).grid(row=0, column=5, sticky="e")

        phases = ttk.Frame(self.root, padding=(14, 0, 14, 8))
        phases.grid(row=1, column=0, sticky="ew")
        for index in range(6):
            phases.columnconfigure(index, weight=1)

        self.extract_button = ttk.Button(phases, text="1. Extraccion", command=self.extract_data)
        self.prepare_button = ttk.Button(phases, text="2. Preparacion", command=self.prepare_data)
        self.train_button = ttk.Button(phases, text="3. Entrenamiento + test", command=self.train_and_test)
        self.infer_button = ttk.Button(phases, text="4. Inferencia", command=self.infer)
        self.plot_button = ttk.Button(phases, text="Abrir grafica", command=self.open_plot)
        self.clear_button = ttk.Button(phases, text="Limpiar log", command=self.clear_log)

        for col, button in enumerate(
            [
                self.extract_button,
                self.prepare_button,
                self.train_button,
                self.infer_button,
                self.plot_button,
                self.clear_button,
            ]
        ):
            button.grid(row=0, column=col, sticky="ew", padx=4)

        summary = ttk.LabelFrame(self.root, text="Estado del flujo", padding=12)
        summary.grid(row=2, column=0, sticky="ew", padx=14, pady=(0, 10))
        for index in range(4):
            summary.columnconfigure(index, weight=1)

        self._metric(summary, 0, "Datos", self.data_var)
        self._metric(summary, 1, "Preparacion", self.features_var)
        self._metric(summary, 2, "Modelo", self.model_var)
        self._metric(summary, 3, "Prediccion", self.prediction_var)

        log_frame = ttk.LabelFrame(self.root, text="Log", padding=8)
        log_frame.grid(row=3, column=0, sticky="nsew", padx=14, pady=(0, 14))
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)

        self.log = Text(log_frame, wrap="word", height=18)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log.yview)
        self.log.configure(yscrollcommand=scrollbar.set)
        self.log.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def _metric(self, parent: ttk.Frame, col: int, title: str, value: StringVar) -> None:
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=col, sticky="ew", padx=8)
        ttk.Label(frame, text=title).pack(anchor="w")
        ttk.Label(frame, textvariable=value, font=("", 12, "bold")).pack(anchor="w")

    def run_all(self) -> None:
        self._run_task("Flujo completo", self._run_all_steps)

    def extract_data(self) -> None:
        self._run_task("Extraccion de datos", self._extract_data)

    def prepare_data(self) -> None:
        self._run_task("Preparacion de datos", self._prepare_data)

    def train_and_test(self) -> None:
        self._run_task("Entrenamiento y test", self._train_and_test)

    def infer(self) -> None:
        self._run_task("Inferencia", self._infer)

    def open_plot(self) -> None:
        if not PLOT_PATH.exists():
            messagebox.showinfo("Grafica no disponible", "Primero ejecuta entrenamiento + test.")
            return
        webbrowser.open(PLOT_PATH.resolve().as_uri())

    def clear_log(self) -> None:
        self.log.delete("1.0", END)

    def _run_task(self, name: str, target) -> None:
        if self.is_running:
            messagebox.showinfo("Proceso en ejecucion", "Espera a que termine la fase actual.")
            return
        self.is_running = True
        self.status_var.set(f"Ejecutando: {name}")
        self._set_buttons_state("disabled")
        thread = threading.Thread(target=self._thread_wrapper, args=(name, target), daemon=True)
        thread.start()

    def _thread_wrapper(self, name: str, target) -> None:
        try:
            self.events.put(("log", f"\n== {name} ==\n"))
            target()
            self.events.put(("done", f"{name} completado"))
        except Exception:
            self.events.put(("error", traceback.format_exc()))

    def _poll_events(self) -> None:
        while True:
            try:
                event, payload = self.events.get_nowait()
            except queue.Empty:
                break

            if event == "log":
                self._append_log(str(payload))
            elif event == "data":
                self.data_var.set(str(payload))
            elif event == "features":
                self.features_var.set(str(payload))
            elif event == "model":
                self.model_var.set(str(payload))
            elif event == "prediction":
                self.prediction_var.set(str(payload))
            elif event == "done":
                self._append_log(f"{payload}\n")
                self.status_var.set("Listo")
                self.is_running = False
                self._set_buttons_state("normal")
            elif event == "error":
                self._append_log(f"ERROR\n{payload}\n")
                self.status_var.set("Error")
                self.is_running = False
                self._set_buttons_state("normal")

        self.root.after(150, self._poll_events)

    def _set_buttons_state(self, state: str) -> None:
        for button in (
            self.extract_button,
            self.prepare_button,
            self.train_button,
            self.infer_button,
            self.plot_button,
            self.clear_button,
        ):
            button.configure(state=state)

    def _append_log(self, text: str) -> None:
        self.log.insert(END, text)
        self.log.see(END)

    def _date_range(self):
        start = parse_date(self.start_var.get().strip())
        end = parse_date(self.end_var.get().strip())
        if start > end:
            raise ValueError("La fecha inicial no puede ser posterior a la fecha final.")
        return start, end

    def _run_all_steps(self) -> None:
        self._extract_data()
        self._prepare_data()
        self._train_and_test()
        self._infer()

    def _extract_data(self) -> pd.DataFrame:
        start, end = self._date_range()
        self.events.put(("log", f"Descargando OMIE desde {start} hasta {end}...\n"))
        data = load_omie_prices(start, end, OmieConfig())
        self.events.put(("data", f"{len(data)} filas en {DATA_PATH}"))
        self.events.put(("log", f"Datos listos: {len(data)} filas, {data['timestamp'].min()} -> {data['timestamp'].max()}\n"))
        return data

    def _load_processed_data(self) -> pd.DataFrame:
        if not DATA_PATH.exists():
            raise FileNotFoundError("No existe data/processed/omie_prices.csv. Ejecuta primero extraccion.")
        return pd.read_csv(DATA_PATH)

    def _prepare_data(self) -> tuple[pd.DataFrame, pd.Series]:
        data = self._load_processed_data()
        self.events.put(("log", "Construyendo variables supervisadas...\n"))
        x, y = make_supervised_dataset(data)
        prepared = x.copy()
        prepared["target_marginal_es"] = y.to_numpy()
        FEATURES_PATH.parent.mkdir(parents=True, exist_ok=True)
        prepared.to_csv(FEATURES_PATH, index=False)
        self.events.put(("features", f"{len(prepared)} filas, {len(x.columns)} variables"))
        self.events.put(("log", f"Dataset preparado guardado en {FEATURES_PATH}\n"))
        return x, y

    def _train_and_test(self):
        data = self._load_processed_data()
        self.events.put(("log", "Entrenando candidatos y evaluando validacion temporal...\n"))
        metrics = train_model(data, MODEL_PATH, PLOT_PATH)
        self.events.put(("model", f"{metrics['best_model']} | MAE {metrics['mae']:.2f}"))
        self.events.put(
            (
                "log",
                (
                    f"Mejor modelo: {metrics['best_model']}\n"
                    f"MAE: {metrics['mae']:.2f} EUR/MWh\n"
                    f"RMSE: {metrics['rmse']:.2f} EUR/MWh\n"
                    f"R2: {metrics['r2']:.3f}\n"
                    f"Baseline lag 24 MAE: {metrics['baseline_lag_24_mae']:.2f} EUR/MWh\n"
                ),
            )
        )
        for name, values in metrics["candidates"].items():
            self.events.put(
                (
                    "log",
                    f"Candidato {name}: MAE {values['mae']:.2f}, RMSE {values['rmse']:.2f}, R2 {values['r2']:.3f}\n",
                )
            )
        self.events.put(("log", f"Modelo guardado en {MODEL_PATH}\nGrafica guardada en {PLOT_PATH}\n"))
        return metrics

    def _infer(self) -> float:
        if not MODEL_PATH.exists():
            raise FileNotFoundError("No existe models/omie_model.joblib. Ejecuta primero entrenamiento + test.")
        data = self._load_processed_data()
        bundle = joblib.load(MODEL_PATH)
        x_next, next_timestamp = make_next_prediction_features(data)
        prediction = float(bundle["model"].predict(x_next)[0])
        text = f"{next_timestamp}: {prediction:.2f} EUR/MWh"
        self.events.put(("prediction", text))
        self.events.put(("log", f"Inferencia: {text}\n"))
        return prediction


def main() -> None:
    root = Tk()
    app = OmiePriceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
