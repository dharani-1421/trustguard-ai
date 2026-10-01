"""Deterministic text cleaning used for both training and inference."""

from __future__ import annotations

import re

_HTML_TAG_RE = re.compile(r"<[^>]+>")
_WHITESPACE_RE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Lowercase, strip HTML tags, collapse whitespace. Does not invent missing content."""
    if text is None:
        return ""
    cleaned = str(text).replace("\x00", " ")
    cleaned = _HTML_TAG_RE.sub(" ", cleaned)
    cleaned = cleaned.lower()
    cleaned = _WHITESPACE_RE.sub(" ", cleaned).strip()
    return cleaned
