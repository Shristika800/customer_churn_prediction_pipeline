from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .config import ModelConfig


@dataclass(frozen=True)
class FeatureBundle:
    features: pd.DataFrame
    target: pd.Series | None


def _required_columns(config: ModelConfig, include_target: bool) -> list[str]:
    columns = [config.id_column, *config.feature_columns]
    if include_target:
        columns.append(config.target_column)
    return columns


def _validate_columns(frame: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required columns: {missing}")


def build_training_bundle(frame: pd.DataFrame, config: ModelConfig) -> FeatureBundle:
    _validate_columns(frame, _required_columns(config, include_target=True))
    return FeatureBundle(
        features=frame[config.feature_columns].copy(),
        target=frame[config.target_column].copy(),
    )


def build_scoring_bundle(frame: pd.DataFrame, config: ModelConfig) -> FeatureBundle:
    _validate_columns(frame, _required_columns(config, include_target=False))
    return FeatureBundle(
        features=frame[config.feature_columns].copy(),
        target=None,
    )
