"""Paths, seeds, and dataset identifiers for the phishing module."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

RANDOM_SEED = 42
TEST_SIZE = 0.20
MODEL_ID = "tfidf-logreg"
MODEL_VERSION = "phishing-tfidf-logreg-v1"

# Zenodo record: Champa, Rabbi & Zibran, "Phishing Email Curated Datasets"
# https://doi.org/10.5281/zenodo.8339691  License: CC BY 4.0
ZENODO_RECORD_ID = "8339691"
ZENODO_DOI = "10.5281/zenodo.8339691"
DATASET_NAME = "Phishing Email Curated Datasets (Nazario + SpamAssassin ham)"
DATASET_LICENSE = "CC BY 4.0"

RAW_DIR = REPO_ROOT / "data" / "raw" / "phishing"
ARTIFACT_DIR = REPO_ROOT / "ml" / "artifacts" / "phishing"
PIPELINE_PATH = ARTIFACT_DIR / "pipeline.joblib"
METRICS_PATH = ARTIFACT_DIR / "metrics.json"
TRAIN_META_PATH = ARTIFACT_DIR / "train_meta.json"

ZENODO_FILES = {
    "Nazario.csv": f"https://zenodo.org/api/records/{ZENODO_RECORD_ID}/files/Nazario.csv/content",
    "SpamAssasin.csv": f"https://zenodo.org/api/records/{ZENODO_RECORD_ID}/files/SpamAssasin.csv/content",
}

# Positive class = Nazario phishing emails.
# Negative class = SpamAssassin rows published as ham (label 0).
# SpamAssassin spam (label 1) is excluded so the positive class is phishing, not generic spam.
NAZARIO_FILENAME = "Nazario.csv"
SPAMASSASSIN_FILENAME = "SpamAssasin.csv"

TEXT_COLUMNS = ("subject", "body")
LABEL_COLUMN = "label"
OPTIONAL_COLUMNS = ("sender",)

TFIDF_MAX_FEATURES = 8000
TFIDF_NGRAM_RANGE = (1, 2)
TFIDF_MIN_DF = 2
LOGREG_MAX_ITER = 200
EXPLANATION_TOP_K = 8
