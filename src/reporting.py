from __future__ import annotations

from io import BytesIO

import pandas as pd


def build_workbook(summary: pd.DataFrame, exact_duplicates: pd.DataFrame) -> BytesIO:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="SUMMARY", index=False)
        exact_duplicates.to_excel(writer, sheet_name="DUPLICATES_EXACT", index=False)
    output.seek(0)
    return output
