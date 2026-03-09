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
- Commands executed locally:
  - `python -m compileall app.py src`
  - `python - <<'PY' ...` (module-level exact dedupe + export smoke test)
- Observations:
  - Exact duplicates populated for repeated normalized rows.
  - Workbook generation succeeded with required tabs.
  - `out/` is listed in `.gitignore`.

## Manual verification checklist
- [ ] Launch Streamlit and upload a small test file.
- [ ] Confirm Exact duplicates table populates.
- [ ] Confirm download works and workbook contains required tabs.
- [x] Confirm `out/` is gitignored.

## Known issues / limitations
- v0.1 only fully implements Exact mode; Column Ignore and Smart Match are intentionally deferred to v0.2/v0.3.
- Manual UI verification is pending human-run Streamlit interaction in this non-interactive environment.
