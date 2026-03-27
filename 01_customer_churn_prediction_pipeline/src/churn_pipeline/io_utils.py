from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def load_training_dataframe(project_root: Path) -> tuple[pd.DataFrame, str]:
    raw_path = project_root / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    sample_path = project_root / "data" / "sample" / "customer_churn_sample.csv"
    if raw_path.exists():
        frame = pd.read_csv(raw_path)
        frame["TotalCharges"] = pd.to_numeric(frame["TotalCharges"], errors="coerce")
        frame["Churn"] = frame["Churn"].map({"Yes": 1, "No": 0})
        return frame, "raw"
    frame = pd.read_csv(sample_path)
    return frame, "sample"


def ensure_artifacts_dir(project_root: Path) -> Path:
    artifacts_dir = project_root / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    return artifacts_dir


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
