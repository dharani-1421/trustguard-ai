"""Compute test-set metrics from a fitted sklearn pipeline. No placeholder numbers."""

from __future__ import annotations

from typing import Dict, List

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline


def evaluate_binary_pipeline(
    pipeline: Pipeline,
    texts: List[str],
    labels: List[int],
) -> Dict:
    if len(texts) == 0:
        raise ValueError("cannot evaluate on an empty test set")
    y_true = np.asarray(labels)
    y_pred = pipeline.predict(texts)
    y_prob = pipeline.predict_proba(texts)[:, 1]
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
    metrics = {
        "n_test": int(len(y_true)),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, pos_label=1, zero_division=0)),
        "confusion_matrix": {
            "labels": [0, 1],
            "matrix": matrix.tolist(),
            "true_negative": int(matrix[0, 0]),
            "false_positive": int(matrix[0, 1]),
            "false_negative": int(matrix[1, 0]),
            "true_positive": int(matrix[1, 1]),
        },
    }
    if len(np.unique(y_true)) == 2:
        metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob))
    else:
        metrics["roc_auc"] = None
        metrics["roc_auc_note"] = "ROC-AUC omitted because the test split contains a single class."
    return metrics
