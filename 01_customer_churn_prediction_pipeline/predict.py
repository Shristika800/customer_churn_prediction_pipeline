from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.churn_pipeline.config import load_model_config
from src.churn_pipeline.inference import load_request_payload, score_payload


PROJECT_ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    config = load_model_config(PROJECT_ROOT)
    payload = load_request_payload(Path(args.input))
    result = score_payload(payload, PROJECT_ROOT / "artifacts" / "model.joblib", config)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
