from pathlib import Path

import pandas as pd

from src.churn_pipeline.config import load_model_config
from src.churn_pipeline.features import build_training_bundle


def test_training_bundle_uses_expected_columns() -> None:
    project_root = Path(__file__).resolve().parents[1]
    config = load_model_config(project_root)
    frame = pd.read_csv(project_root / "data" / "sample" / "customer_churn_sample.csv")
    bundle = build_training_bundle(frame, config)
    assert list(bundle.features.columns) == config.feature_columns
    assert bundle.target is not None
