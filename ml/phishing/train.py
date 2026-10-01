"""Train TF-IDF + logistic regression and persist artefacts only after evaluation."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from ml.phishing.config import (
    ARTIFACT_DIR,
    DATASET_LICENSE,
    DATASET_NAME,
    LOGREG_MAX_ITER,
    METRICS_PATH,
    MODEL_ID,
    MODEL_VERSION,
    NAZARIO_FILENAME,
    PIPELINE_PATH,
    RANDOM_SEED,
    RAW_DIR,
    SPAMASSASSIN_FILENAME,
    TEST_SIZE,
    TFIDF_MAX_FEATURES,
    TFIDF_MIN_DF,
    TFIDF_NGRAM_RANGE,
    TRAIN_META_PATH,
    ZENODO_DOI,
)
from ml.phishing.data_loader import download_zenodo_files, file_md5, load_training_frame
from ml.phishing.evaluate import evaluate_binary_pipeline
from ml.phishing.preprocess import clean_text


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    preprocessor=clean_text,
                    lowercase=False,
                    ngram_range=TFIDF_NGRAM_RANGE,
                    max_features=TFIDF_MAX_FEATURES,
                    min_df=TFIDF_MIN_DF,
                    stop_words="english",
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    max_iter=LOGREG_MAX_ITER,
                    class_weight="balanced",
                    solver="liblinear",
                    random_state=RANDOM_SEED,
                ),
            ),
        ]
    )


def train_and_evaluate(
    raw_dir: Path = RAW_DIR,
    artifact_dir: Path = ARTIFACT_DIR,
    download: bool = False,
) -> Dict:
    if download:
        download_zenodo_files(raw_dir)

    frame, reports = load_training_frame(raw_dir)
    texts: List[str] = frame["text"].tolist()
    labels: List[int] = frame["label"].astype(int).tolist()

    x_train, x_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=labels,
    )

    pipeline = build_pipeline()
    pipeline.fit(x_train, y_train)
    metrics = evaluate_binary_pipeline(pipeline, x_test, y_test)

    artifact_dir.mkdir(parents=True, exist_ok=True)
    pipeline_path = artifact_dir / "pipeline.joblib"
    metrics_path = artifact_dir / "metrics.json"
    meta_path = artifact_dir / "train_meta.json"

    joblib.dump(
        {
            "pipeline": pipeline,
            "model_id": MODEL_ID,
            "model_version": MODEL_VERSION,
            "label_map": {0: "legitimate", 1: "phishing"},
        },
        pipeline_path,
    )

    source_files = {}
    for name in (NAZARIO_FILENAME, SPAMASSASSIN_FILENAME):
        path = raw_dir / name
        if path.exists():
            source_files[name] = {
                "path": str(path),
                "bytes": path.stat().st_size,
                "md5": file_md5(path),
            }

    payload = {
        "model_id": MODEL_ID,
        "model_version": MODEL_VERSION,
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "dataset": {
            "name": DATASET_NAME,
            "doi": ZENODO_DOI,
            "license": DATASET_LICENSE,
            "files": source_files,
        },
        "split": {
            "test_size": TEST_SIZE,
            "random_seed": RANDOM_SEED,
            "stratified": True,
            "n_train": len(x_train),
            "n_test": len(x_test),
            "n_train_phishing": int(sum(y_train)),
            "n_train_legitimate": int(len(y_train) - sum(y_train)),
            "n_test_phishing": int(sum(y_test)),
            "n_test_legitimate": int(len(y_test) - sum(y_test)),
        },
        "algorithm": {
            "vectorizer": "TfidfVectorizer",
            "ngram_range": list(TFIDF_NGRAM_RANGE),
            "max_features": TFIDF_MAX_FEATURES,
            "min_df": TFIDF_MIN_DF,
            "classifier": "LogisticRegression",
            "solver": "liblinear",
            "class_weight": "balanced",
        },
        "metrics": metrics,
        "validation_reports": [report.as_dict() for report in reports],
    }
    metrics_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    meta_path.write_text(
        json.dumps(
            {
                "model_version": MODEL_VERSION,
                "pipeline_path": str(pipeline_path),
                "metrics_path": str(metrics_path),
                "n_rows_total": int(len(frame)),
                "class_counts": {
                    "legitimate": int((frame["label"] == 0).sum()),
                    "phishing": int((frame["label"] == 1).sum()),
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return payload


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Train the TrustGuard phishing baseline.")
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download Nazario.csv and SpamAssasin.csv from Zenodo if missing.",
    )
    args = parser.parse_args(argv)
    result = train_and_evaluate(download=args.download)
    print(json.dumps(result["metrics"], indent=2))
    print(f"Saved pipeline to {PIPELINE_PATH}")
    print(f"Saved evaluation to {METRICS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
