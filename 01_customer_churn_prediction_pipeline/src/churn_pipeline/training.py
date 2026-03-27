from __future__ import annotations

from dataclasses import dataclass

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import ModelConfig


@dataclass(frozen=True)
class TrainingOutputs:
    model_pipeline: Pipeline
    metrics: dict[str, object]
    metadata: dict[str, object]


def build_model_pipeline(config: ModelConfig) -> Pipeline:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, config.numeric_features),
            ("categorical", categorical_pipeline, config.categorical_features),
        ]
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=250, max_depth=6, random_state=42)),
        ]
    )


def train_model(features: pd.DataFrame, target: pd.Series, config: ModelConfig) -> TrainingOutputs:
    X_train, X_valid, y_train, y_valid = train_test_split(
        features,
        target,
        test_size=0.25,
        random_state=42,
        stratify=target,
    )
    pipeline = build_model_pipeline(config)
    pipeline.fit(X_train, y_train)
    probabilities = pipeline.predict_proba(X_valid)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    metrics = {
        "train_rows": int(len(X_train)),
        "validation_rows": int(len(X_valid)),
        "accuracy": round(float(accuracy_score(y_valid, predictions)), 4),
        "precision": round(float(precision_score(y_valid, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_valid, predictions, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_valid, probabilities)), 4),
    }
    metadata = {
        "model_type": "random_forest_classifier",
        "threshold": 0.5,
        "feature_columns": config.feature_columns,
    }
    return TrainingOutputs(pipeline, metrics, metadata)


def save_model(path, pipeline: Pipeline) -> None:
    joblib.dump(pipeline, path)
