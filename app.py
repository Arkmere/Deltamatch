from __future__ import annotations

import pandas as pd
import streamlit as st

from src.dedupe_exact import find_exact_duplicates
from src.io import list_excel_sheets, load_dataframe
from src.reporting import build_workbook
from src.utils import config_fingerprint

st.set_page_config(page_title="DeltaMatch", layout="wide")
st.title("DeltaMatch")
st.caption("Universal, intelligent deduplication for Excel and CSV files")

st.sidebar.header("Configuration")
uploaded = st.sidebar.file_uploader("Upload file", type=["csv", "xlsx"])

normalize_config = {
    "case_insensitive": st.sidebar.checkbox("Case-insensitive", value=True),
    "trim": st.sidebar.checkbox("Trim", value=True),
    "collapse_whitespace": st.sidebar.checkbox("Collapse whitespace", value=True),
    "treat_dash_as_blank": st.sidebar.checkbox("Treat '-' as blank", value=True),
}

mode = st.sidebar.radio("Mode", ["Exact", "Column Ignore", "Smart Match (UNKN-fill)"])

sheet_name = None
if uploaded is not None and uploaded.name.lower().endswith(".xlsx"):
    sheets = list_excel_sheets(uploaded)
    sheet_name = st.sidebar.selectbox("Sheet", sheets, index=0)

if uploaded is None:
    st.info("Upload a CSV or XLSX file to begin.")
    st.stop()

try:
    df = load_dataframe(uploaded, uploaded.name, sheet_name=sheet_name)
except Exception as exc:
    st.error(f"Failed to load file: {exc}")
    st.stop()

st.subheader("Input preview")
st.dataframe(df.head(50), use_container_width=True)

if mode != "Exact":
    st.warning("This milestone currently implements Exact mode. Other modes are planned for upcoming PRs.")

exact_df = find_exact_duplicates(df, normalize_config)

rows_scanned = len(df)
duplicate_groups = exact_df["dup_group_id"].nunique() if not exact_df.empty else 0
rows_involved = len(exact_df)

col1, col2, col3 = st.columns(3)
col1.metric("Rows scanned", rows_scanned)
col2.metric("Duplicate groups found", duplicate_groups)
col3.metric("Rows involved", rows_involved)

results_tab = st.tabs(["Exact Duplicates"])[0]
with results_tab:
    st.dataframe(exact_df, use_container_width=True)

summary_df = pd.DataFrame(
    [
        {
            "metric": "rows_scanned",
            "value": rows_scanned,
        },
        {
            "metric": "duplicate_groups_found",
            "value": duplicate_groups,
        },
        {
            "metric": "rows_involved",
            "value": rows_involved,
        },
        {
            "metric": "mode",
            "value": mode,
        },
        {
            "metric": "normalization_config",
            "value": str(normalize_config),
        },
        {
            "metric": "config_fingerprint",
            "value": config_fingerprint({"mode": mode, **normalize_config, "sheet_name": sheet_name}),
        },
    ]
)

workbook = build_workbook(summary_df, exact_df)

st.download_button(
    "Process and Download",
    data=workbook,
    file_name="deltamatch_results.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
