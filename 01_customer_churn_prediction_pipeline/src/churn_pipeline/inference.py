from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd

from .config import ModelConfig
from .features import build_scoring_bundle


def load_request_payload(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def score_payload(payload: dict[str, object], model_path: Path, config: ModelConfig) -> dict[str, object]:
    pipeline = joblib.load(model_path)
    frame = pd.DataFrame([payload])
    bundle = build_scoring_bundle(frame, config)
    probability = float(pipeline.predict_proba(bundle.features)[0][1])
    return {
        "customerID": str(payload[config.id_column]),
        "churn_probability": round(probability, 4),
        "predicted_label": int(probability >= 0.5),
    }
