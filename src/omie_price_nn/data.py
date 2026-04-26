from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import requests


OMIE_DOWNLOAD_URL = "https://www.omie.es/es/file-download"


@dataclass(frozen=True)
class OmieConfig:
    raw_dir: Path = Path("data/raw")
    processed_dir: Path = Path("data/processed")
    timeout_seconds: int = 30


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def iter_days(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def omie_filename(day: date) -> str:
    return f"marginalpdbc_{day:%Y%m%d}.1"


def download_daily_file(day: date, config: OmieConfig) -> Path:
    config.raw_dir.mkdir(parents=True, exist_ok=True)
    destination = config.raw_dir / omie_filename(day)
    if destination.exists() and destination.stat().st_size > 0:
        return destination

    response = requests.get(
        OMIE_DOWNLOAD_URL,
        params={"parents[0]": "marginalpdbc", "filename": destination.name},
        timeout=config.timeout_seconds,
    )
    response.raise_for_status()

    text = response.text.strip()
    if "MARGINALPDBC" not in text:
        raise ValueError(f"OMIE did not return a MARGINALPDBC file for {day}: {text[:120]}")

    destination.write_text(response.text, encoding=response.encoding or "utf-8")
    return destination


def parse_marginalpdbc(path: Path) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("MARGINALPDBC") or line.startswith("*"):
            continue

        parts = [part.strip() for part in line.split(";") if part.strip()]
        if len(parts) < 6:
            continue

        year, month, day, period = map(int, parts[:4])
        marginal_pt = float(parts[4].replace(",", "."))
        marginal_es = float(parts[5].replace(",", "."))
        session_day = date(year, month, day)

        rows.append(
            {
                "date": session_day,
                "period": period,
                "timestamp": pd.Timestamp(session_day),
                "marginal_pt": marginal_pt,
                "marginal_es": marginal_es,
            }
        )

    if not rows:
        raise ValueError(f"No price rows found in {path}")

    df = pd.DataFrame(rows).sort_values(["date", "period"]).reset_index(drop=True)
    periods_per_day = df.groupby("date")["period"].transform("max")
    interval_minutes = periods_per_day.map(lambda periods: 15 if periods > 25 else 60)
    df["timestamp"] = pd.to_datetime(df["date"]) + pd.to_timedelta(
        (df["period"] - 1) * interval_minutes, unit="m"
    )
    return df.sort_values("timestamp").reset_index(drop=True)


def load_omie_prices(start: date, end: date, config: OmieConfig | None = None) -> pd.DataFrame:
    config = config or OmieConfig()
    frames = []
    failures = []

    for day in iter_days(start, end):
        try:
            file_path = download_daily_file(day, config)
            frames.append(parse_marginalpdbc(file_path))
        except Exception as exc:  # keep long date ranges usable if one daily file is missing
            failures.append(f"{day}: {exc}")

    if not frames:
        details = "\n".join(failures[:5])
        raise RuntimeError(f"No OMIE files could be loaded.\n{details}")

    data = pd.concat(frames, ignore_index=True)
    data = data.drop_duplicates(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)

    config.processed_dir.mkdir(parents=True, exist_ok=True)
    data.to_csv(config.processed_dir / "omie_prices.csv", index=False)

    if failures:
        print(f"Warning: skipped {len(failures)} day(s). First issue: {failures[0]}")

    return data
