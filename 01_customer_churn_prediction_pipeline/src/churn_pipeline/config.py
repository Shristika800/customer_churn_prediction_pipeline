from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelConfig:
    id_column: str
    target_column: str
    numeric_features: list[str]
    categorical_features: list[str]

    @property
    def feature_columns(self) -> list[str]:
        return self.numeric_features + self.categorical_features


def load_model_config(project_root: Path) -> ModelConfig:
    payload = json.loads((project_root / "config" / "model_config.json").read_text(encoding="utf-8"))
    return ModelConfig(
        id_column=payload["id_column"],
        target_column=payload["target_column"],
        numeric_features=payload["numeric_features"],
        categorical_features=payload["categorical_features"],
    )
