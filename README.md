# DeltaMatch

DeltaMatch is a local Streamlit tool for deterministic dataset deduplication.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## v0.1 scope

- File upload for CSV/XLSX (with sheet selector for XLSX).
- Exact duplicate detection after normalization.
- Deterministic group IDs and stable sorting.
- One-click XLSX export with `SUMMARY` and `DUPLICATES_EXACT` sheets.

## Privacy

All processing is local. Generated outputs should remain uncommitted (`out/` is gitignored).
