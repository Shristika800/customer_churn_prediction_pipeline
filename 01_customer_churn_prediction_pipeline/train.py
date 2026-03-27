from __future__ import annotations

from pathlib import Path

from src.churn_pipeline.config import load_model_config
from src.churn_pipeline.features import build_training_bundle
from src.churn_pipeline.io_utils import ensure_artifacts_dir, load_training_dataframe, write_json
from src.churn_pipeline.training import save_model, train_model


PROJECT_ROOT = Path(__file__).resolve().parent


def main() -> None:
    config = load_model_config(PROJECT_ROOT)
    frame, source = load_training_dataframe(PROJECT_ROOT)
    bundle = build_training_bundle(frame, config)
    outputs = train_model(bundle.features, bundle.target, config)
    artifacts_dir = ensure_artifacts_dir(PROJECT_ROOT)
    save_model(artifacts_dir / "model.joblib", outputs.model_pipeline)
    write_json(artifacts_dir / "train_metrics.json", {**outputs.metrics, "data_source": source})
    write_json(artifacts_dir / "model_metadata.json", outputs.metadata)
    print("training complete")
    print(outputs.metrics)


if __name__ == "__main__":
    main()
