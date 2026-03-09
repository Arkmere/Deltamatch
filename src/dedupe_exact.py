from __future__ import annotations

import pandas as pd

from src.normalize import normalize_series
from src.utils import make_exact_group_id, sha256_text


def find_exact_duplicates(df: pd.DataFrame, normalize_config: dict) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["dup_group_id", "row_index", "row_hash"])

    normalized = pd.DataFrame({col: normalize_series(df[col], normalize_config) for col in df.columns})
    joined = normalized.astype(str).agg("|".join, axis=1)
    row_hashes = joined.apply(sha256_text)

    work = pd.DataFrame(
        {
            "row_index": df.index,
            "row_hash": row_hashes,
        }
    )
    counts = work.groupby("row_hash")["row_hash"].transform("size")
    dups = work[counts > 1].copy()
    dups["dup_group_id"] = dups["row_hash"].apply(make_exact_group_id)
    dups = dups.sort_values(["dup_group_id", "row_index"], kind="mergesort")
    return dups[["dup_group_id", "row_index", "row_hash"]].reset_index(drop=True)
