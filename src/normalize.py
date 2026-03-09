from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any, Dict

import pandas as pd

_WHITESPACE_RE = re.compile(r"\s+")


def normalize_cell(value: Any, config: Dict[str, Any]) -> str:
    """Normalize one cell value to a deterministic string representation."""
    if value is None or (isinstance(value, float) and pd.isna(value)) or pd.isna(value):
        normalized = ""
    elif isinstance(value, (pd.Timestamp, datetime, date)):
        normalized = pd.Timestamp(value).isoformat()
    else:
        normalized = str(value)

    if config.get("trim", True):
        normalized = normalized.strip()
    if config.get("collapse_whitespace", True):
        normalized = _WHITESPACE_RE.sub(" ", normalized)
    if config.get("treat_dash_as_blank", True) and normalized == "-":
        normalized = ""
    if config.get("case_insensitive", True):
        normalized = normalized.upper()
    return normalized


def normalize_series(series: pd.Series, config: Dict[str, Any]) -> pd.Series:
    return series.apply(lambda v: normalize_cell(v, config))


def is_unknown(normalized_value: str, unknown_tokens_set: set[str]) -> bool:
    return normalized_value in unknown_tokens_set
