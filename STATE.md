# DeltaMatch STATE Ledger

## Purpose and roles
- **Manager (PM): Stuart** — coordination, priorities, releases.
- **Solutions Architect & QA Lead: ChatGPT** — tickets, audits, risk management.
- **Production Engineer: Codex** — implementation and ledger updates.

## Scope
Build a local Streamlit deduplication tool with milestone PRs (`v0.1` to `v0.4`) and deterministic matching IDs.

## Milestone plan
- [x] **v0.1** Scaffold + Load + Exact Duplicates + Export
- [ ] **v0.2** Column Ignore Mode + Dynamic Column Selectors
- [ ] **v0.3** Smart Match (UNKN-fill) + Diff Viewer + Why column + Large File Warning
- [ ] **v0.4** Polish + Determinism Hardening + Date Auto-cast + Documentation

## Current Sprint
- Delivering **v0.1** implementation with exact duplicate detection and XLSX export.

## v0.1 Status
- **GREEN (verified + deterministic)**

## Decisions
- Normalization defaults are ON: case-insensitive, trim, collapse whitespace, treat `-` as blank.
- Exact duplicate hashing uses SHA-256 over joined normalized row values.
- Deterministic exact group ID: `EXACT_` + first 8 chars of `sha256(row_hash)`.
- Stable output ordering: sort by `(dup_group_id, row_index)`.

## Completed work
- **2026-03-09**: Implemented v0.1 scaffold, Streamlit UI, exact dedupe engine, and export workbook tabs (`SUMMARY`, `DUPLICATES_EXACT`).
  - PR: _TBD_
  - Files touched: `app.py`, `src/io.py`, `src/normalize.py`, `src/dedupe_exact.py`, `src/reporting.py`, `src/utils.py`, `requirements.txt`, `.gitignore`, `README.md`, `STATE.md`.
  - How to run:
    1. `python -m venv .venv`
    2. `source .venv/bin/activate`
    3. `pip install -r requirements.txt`
    4. `streamlit run app.py`

## Evidence (v0.1)
- Initial commands executed:
  - `python -m compileall app.py src`
  - `python - <<'PY' ...` (module-level exact dedupe + export smoke test)
- Verification entry (**2026-03-09**, UTC):
  - Environment:
    - Windows PowerShell
    - Version commands used:
      - `python --version`
      - `python -c "import streamlit; print(streamlit.__version__)"`
    - Observed output (copy/paste):
      - `Python 3.10.19`
      - `ModuleNotFoundError: No module named 'streamlit'`
  - Test dataset:
    - `golden.csv`
    - Rows scanned: `4`
    - Normalisation toggles enabled: case-insensitive, trim, collapse whitespace, treat `'-'` as blank
  - Observed Exact mode results:
    - Duplicate groups found: `1`
    - Rows involved: `4`
    - `dup_group_id`: `EXACT_324849b5`
    - `row_hash` identical across all 4 rows
  - Export verification:
    - Workbook tabs present: `SUMMARY`, `DUPLICATES_EXACT`
    - `SUMMARY` includes `config_fingerprint`
  - Determinism verification (rerun compare):
    - Compared `deltamatch_results.xlsx` vs `deltamatch_results (1).xlsx`
    - Same tabs in both files
    - Same `config_fingerprint`
    - Same `dup_group_id` (`EXACT_324849b5`)
    - Same `row_hash` values
    - Outputs were identical across reruns

## Manual verification checklist
- [x] Launch Streamlit and upload a small test file.
- [x] Confirm Exact duplicates table populates.
- [x] Confirm download works and workbook contains required tabs.
- [x] Confirm `out/` is gitignored.

## Next milestone (v0.2) stub
- [ ] Column Ignore mode UI (dynamic column selector)
- [ ] Ignore-columns hashing/grouping
- [ ] Export adds `DUPLICATES_IGNORE`
- [ ] v0.2 verification with `golden_ignore.csv`

## Known issues / limitations
- v0.1 only fully implements Exact mode; Column Ignore and Smart Match are intentionally deferred to v0.2/v0.3.
- Smart Match runtime is expected to scale with entity-group sizes (to be quantified in later milestones).
