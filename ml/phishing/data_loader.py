"""Load and validate the documented public phishing email CSVs."""

from __future__ import annotations

import hashlib
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Sequence

import pandas as pd

from ml.phishing.config import (
    LABEL_COLUMN,
    NAZARIO_FILENAME,
    RAW_DIR,
    SPAMASSASSIN_FILENAME,
    TEXT_COLUMNS,
    ZENODO_FILES,
)

POSITIVE_LABELS = {1, "1", "phishing", "phish"}
NEGATIVE_LABELS = {0, "0", "ham", "legitimate", "legit"}


class DatasetValidationError(ValueError):
    """Raised when a CSV cannot be used without inventing or guessing values."""


@dataclass
class ValidationReport:
    source: str
    rows_read: int
    rows_kept: int
    missing_required_columns: List[str] = field(default_factory=list)
    dropped_missing_label: int = 0
    dropped_empty_text: int = 0
    dropped_duplicates: int = 0
    unknown_label_values: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict:
        return {
            "source": self.source,
            "rows_read": self.rows_read,
            "rows_kept": self.rows_kept,
            "missing_required_columns": self.missing_required_columns,
            "dropped_missing_label": self.dropped_missing_label,
            "dropped_empty_text": self.dropped_empty_text,
            "dropped_duplicates": self.dropped_duplicates,
            "unknown_label_values": self.unknown_label_values,
            "notes": self.notes,
        }


def download_zenodo_files(raw_dir: Path = RAW_DIR, timeout: int = 180) -> List[Path]:
    """Download the documented Zenodo CSVs if they are not already present."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    saved: List[Path] = []
    for filename, url in ZENODO_FILES.items():
        path = raw_dir / filename
        if path.exists() and path.stat().st_size > 0:
            saved.append(path)
            continue
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "TrustGuardAI/0.1 (hackathon research prototype)"},
        )
        with urllib.request.urlopen(request, timeout=timeout) as response, path.open("wb") as handle:
            while True:
                chunk = response.read(256 * 1024)
                if not chunk:
                    break
                handle.write(chunk)
        saved.append(path)
    return saved


def _require_columns(frame: pd.DataFrame, source: str) -> None:
    required = [LABEL_COLUMN, *TEXT_COLUMNS]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise DatasetValidationError(
            f"{source}: missing required columns {missing}. Found {list(frame.columns)}"
        )


def _map_label(value) -> int:
    if pd.isna(value):
        raise DatasetValidationError("missing label")
    if isinstance(value, str):
        candidate = value.strip().lower()
        if candidate in ("1", "phishing", "phish"):
            return 1
        if candidate in ("0", "ham", "legitimate", "legit"):
            return 0
        raise DatasetValidationError(f"unknown label: {value!r}")
    numeric = int(value)
    if numeric == 1:
        return 1
    if numeric == 0:
        return 0
    raise DatasetValidationError(f"unknown label: {value!r}")


def combine_email_text(subject: str = "", body: str = "", sender: str = "") -> str:
    """Combine fields the same way at train time and inference time."""
    parts: List[str] = []
    sender = (sender or "").strip()
    subject = (subject or "").strip()
    body = (body or "").strip()
    if sender:
        parts.append(f"From: {sender}")
    if subject:
        parts.append(f"Subject: {subject}")
    if body:
        parts.append(body)
    return "\n".join(parts).strip()


def _combined_text_series(frame: pd.DataFrame) -> pd.Series:
    def row_text(row: pd.Series) -> str:
        subject = str(row["subject"]) if "subject" in row.index and pd.notna(row["subject"]) else ""
        body = str(row["body"]) if "body" in row.index and pd.notna(row["body"]) else ""
        sender = str(row["sender"]) if "sender" in row.index and pd.notna(row["sender"]) else ""
        return combine_email_text(subject=subject, body=body, sender=sender)

    return frame.apply(row_text, axis=1)


def validate_and_normalize(
    frame: pd.DataFrame,
    source: str,
    allowed_labels: Sequence[int] | None = None,
) -> tuple[pd.DataFrame, ValidationReport]:
    """Validate a raw curated CSV and return text/label rows. Does not impute labels or text."""
    report = ValidationReport(source=source, rows_read=len(frame), rows_kept=0)
    _require_columns(frame, source)

    working = frame.copy()
    original_labels = working[LABEL_COLUMN]
    missing_label_mask = original_labels.isna() | original_labels.astype(str).str.strip().eq("")
    report.dropped_missing_label = int(missing_label_mask.sum())
    working = working.loc[~missing_label_mask]

    mapped: List[int] = []
    unknown: List[str] = []
    keep_index = []
    for idx, value in working[LABEL_COLUMN].items():
        try:
            mapped.append(_map_label(value))
            keep_index.append(idx)
        except DatasetValidationError:
            unknown.append(repr(value))
    if unknown:
        unique_unknown = sorted(set(unknown))
        report.unknown_label_values = unique_unknown
        raise DatasetValidationError(
            f"{source}: unknown label values {unique_unknown}. Refusing to guess."
        )
    working = working.loc[keep_index]
    working = working.assign(label=mapped)

    if allowed_labels is not None:
        allowed = set(allowed_labels)
        working = working.loc[working["label"].isin(allowed)]
        report.notes.append(f"kept labels {sorted(allowed)} only")

    working = working.assign(text=_combined_text_series(working))
    empty_mask = working["text"].str.strip().eq("")
    report.dropped_empty_text = int(empty_mask.sum())
    working = working.loc[~empty_mask]

    before_dedupe = len(working)
    working = working.drop_duplicates(subset=["text", "label"])
    report.dropped_duplicates = before_dedupe - len(working)

    normalized = working[["text", "label"]].reset_index(drop=True)
    report.rows_kept = len(normalized)
    if report.rows_kept == 0:
        raise DatasetValidationError(f"{source}: no usable rows after validation")
    return normalized, report


def load_training_frame(raw_dir: Path = RAW_DIR) -> tuple[pd.DataFrame, List[ValidationReport]]:
    """
    Build the training table:

    - Nazario.csv → phishing (label 1), all valid rows
    - SpamAssasin.csv → legitimate (label 0) only

    SpamAssassin spam rows are dropped, not relabelled as phishing.
    """
    nazario_path = raw_dir / NAZARIO_FILENAME
    ham_path = raw_dir / SPAMASSASSIN_FILENAME
    missing = [str(path) for path in (nazario_path, ham_path) if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Public dataset files are missing. Run `python -m ml.phishing.train --download` "
            f"or place the Zenodo CSVs in {raw_dir}. Missing: {missing}"
        )

    nazario_raw = pd.read_csv(nazario_path)
    ham_raw = pd.read_csv(ham_path)
    nazario, nazario_report = validate_and_normalize(
        nazario_raw, NAZARIO_FILENAME, allowed_labels=(0, 1)
    )
    # Nazario is a phishing corpus; keep only published positives if mixed.
    if set(nazario["label"].unique()) == {1}:
        nazario_report.notes.append("all rows labelled phishing")
    else:
        before = len(nazario)
        nazario = nazario.loc[nazario["label"] == 1]
        nazario_report.notes.append(
            f"kept {len(nazario)} phishing rows; dropped {before - len(nazario)} non-phishing rows"
        )
        nazario_report.rows_kept = len(nazario)

    ham, ham_report = validate_and_normalize(
        ham_raw, SPAMASSASSIN_FILENAME, allowed_labels=(0,)
    )
    ham_report.notes.append("SpamAssassin spam (label 1) excluded by design")

    combined = pd.concat([nazario, ham], ignore_index=True)
    before_dedupe = len(combined)
    combined = combined.drop_duplicates(subset=["text", "label"]).reset_index(drop=True)
    cross_dupes = before_dedupe - len(combined)

    if combined["label"].nunique() < 2:
        raise DatasetValidationError("training data must contain both legitimate and phishing labels")

    reports = [nazario_report, ham_report]
    if cross_dupes:
        reports.append(
            ValidationReport(
                source="combined",
                rows_read=before_dedupe,
                rows_kept=len(combined),
                dropped_duplicates=cross_dupes,
                notes=["duplicates across sources removed"],
            )
        )
    return combined, reports


def file_md5(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
