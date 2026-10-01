"""Inference and linear-model feature contributions for a single email."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

import joblib
import numpy as np
from sklearn.pipeline import Pipeline

from ml.phishing.config import (
    ARTIFACT_DIR,
    EXPLANATION_TOP_K,
    METRICS_PATH,
    MODEL_ID,
    MODEL_VERSION,
    PIPELINE_PATH,
)
from ml.phishing.data_loader import combine_email_text


class ModelNotTrainedError(FileNotFoundError):
    """Raised when inference is requested before artefacts exist."""


def load_bundle(artifact_dir: Optional[Path] = None) -> Dict:
    path = (artifact_dir or ARTIFACT_DIR) / "pipeline.joblib"
    if artifact_dir is None:
        path = PIPELINE_PATH
    if not path.exists():
        raise ModelNotTrainedError(
            f"No trained phishing model at {path}. Run: python -m ml.phishing.train --download"
        )
    return joblib.load(path)


@lru_cache(maxsize=1)
def _cached_bundle() -> Dict:
    return load_bundle()


def clear_model_cache() -> None:
    _cached_bundle.cache_clear()


def load_evaluation(metrics_path: Path = METRICS_PATH) -> Optional[Dict]:
    if not metrics_path.exists():
        return None
    return json.loads(metrics_path.read_text(encoding="utf-8"))


def _feature_contributions(
    pipeline: Pipeline,
    raw_text: str,
    predicted_class: int,
    top_k: int = EXPLANATION_TOP_K,
) -> List[Dict]:
    """
    Contribution of each n-gram is coef[i] * tfidf[i] for the phishing class (label 1).

    This is the linear model itself, not a separate explainer.
    """
    vectorizer = pipeline.named_steps["tfidf"]
    classifier = pipeline.named_steps["clf"]
    transformed = vectorizer.transform([raw_text])
    coefficients = classifier.coef_[0]
    feature_names = vectorizer.get_feature_names_out()
    row = transformed.tocoo()
    scored = []
    for col, value in zip(row.col, row.data):
        contribution = float(coefficients[col] * value)
        scored.append(
            {
                "feature": str(feature_names[col]),
                "tfidf": float(value),
                "coefficient": float(coefficients[col]),
                "contribution_to_phishing": contribution,
            }
        )
    if predicted_class == 1:
        scored.sort(key=lambda item: item["contribution_to_phishing"], reverse=True)
    else:
        scored.sort(key=lambda item: item["contribution_to_phishing"])
    return scored[:top_k]


def analyze_email(
    subject: str = "",
    body: str = "",
    sender: str = "",
    artifact_dir: Optional[Path] = None,
) -> Dict:
    combined = combine_email_text(subject=subject, body=body, sender=sender)
    if not combined:
        raise ValueError("subject and body are empty; nothing to classify")

    bundle = load_bundle(artifact_dir) if artifact_dir is not None else _cached_bundle()
    pipeline: Pipeline = bundle["pipeline"]
    label_map: Dict[int, str] = bundle.get("label_map") or {0: "legitimate", 1: "phishing"}
    model_id = bundle.get("model_id", MODEL_ID)
    model_version = bundle.get("model_version", MODEL_VERSION)

    predicted = int(pipeline.predict([combined])[0])
    probabilities = pipeline.predict_proba([combined])[0]
    prediction = label_map[predicted]
    return {
        "prediction": prediction,
        "predicted_label": predicted,
        "probability": float(probabilities[predicted]),
        "probability_phishing": float(probabilities[1]),
        "probability_legitimate": float(probabilities[0]),
        "probability_type": "logistic_regression_predict_proba",
        "model": model_id,
        "model_version": model_version,
        "explanation": _feature_contributions(pipeline, combined, predicted),
        "threat_status": "suspicious" if predicted == 1 else "no_phishing_indicated",
        "input_used": {
            "combined_fields": ["sender", "subject", "body"],
            "character_count": len(combined),
        },
    }
