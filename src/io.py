from __future__ import annotations

from io import BytesIO
from typing import BinaryIO

import pandas as pd


def list_excel_sheets(file_obj: BinaryIO) -> list[str]:
    file_obj.seek(0)
    excel_file = pd.ExcelFile(file_obj, engine="openpyxl")
    return excel_file.sheet_names


def load_dataframe(file_obj: BinaryIO, filename: str, sheet_name: str | None = None) -> pd.DataFrame:
    file_obj.seek(0)
    lower = filename.lower()
    if lower.endswith(".csv"):
        return pd.read_csv(file_obj)
    if lower.endswith(".xlsx"):
        return pd.read_excel(file_obj, sheet_name=sheet_name, engine="openpyxl")
    raise ValueError("Unsupported file type. Please upload CSV or XLSX.")
