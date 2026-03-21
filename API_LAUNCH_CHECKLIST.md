# API launch checklist

This checklist is intended for the first transition from manual validation to live API-backed weekly observation.

Its purpose is not to expand the system further, but to ensure that the first live runs remain stable, comparable, and easy to interpret.

## 1. Secrets and credentials

- [ ] Required API key has been added to GitHub Secrets
- [ ] Secret name matches the workflow expectation exactly
- [ ] Any non-OpenAI market-reference keys or public endpoints have been checked
- [ ] No API key is hardcoded in scripts or tracked files

## 2. Observation core stability

- [ ] Fixed prompt is unchanged from the current validated version
- [ ] Core output schema is unchanged
- [ ] Core field names are unchanged
- [ ] Weekly output format remains stable enough for comparison
- [ ] No untested prompt changes are bundled into the first live run

## 3. Workflow and scripts

- [ ] `.github/workflows/weekly_observation.yml` points to the correct scripts
- [ ] `run_weekly.py` is still the intended entry point for discourse generation
- [ ] `score_outputs.py` still writes summaries without schema mismatch
- [ ] `plot_master_summary.py` still reads the latest summary correctly
- [ ] `fetch_market_reference.py` still appends without breaking the CSV structure
- [ ] `plot_market_reference.py` and `plot_market_reference_normalized.py` still render successfully

## 4. File and schema consistency

- [ ] `data/market_reference.csv` column order is fixed and documented
- [ ] Asset names are fixed and spelled consistently
- [ ] Unit names are fixed and spelled consistently
- [ ] Date format is consistently `YYYY-MM-DD`
- [ ] Mixed-source rows are still readable through `source_note`
- [ ] Duplicate `(date, asset)` rows are prevented or intentionally handled

## 5. Notes and measurement readiness

- [ ] `notes/weekly_memo_YYYY-MM-DD.md` template is ready
- [ ] `measurements/discourse_sidecar.csv` is ready for a new row
- [ ] `measurements/scoring_rubric.md` is present
- [ ] `measurements/lexical_candidates.md` is present
- [ ] The first live memo filename has been decided in advance

## 6. First live-run plan

- [ ] First live run date has been decided
- [ ] The first live run will be treated as a baseline run, not a major interpretation run
- [ ] Any interpretation written after the first run will be marked as provisional
- [ ] No major market-lane expansion will be added during the first live run
- [ ] No schema redesign will be attempted during the first live run

## 7. Interpretation discipline

- [ ] External market lanes are treated as comparison lanes, not causal proof
- [ ] Weekly memos remain interpretive, comparative, and non-causal
- [ ] Early sidecar scores remain provisional rather than canonical
- [ ] Any new measurement dimensions remain outside the core schema until stable

## 8. Success condition for launch

The launch is considered successful if:

- the workflow completes without structural errors
- the live output can be read using the current schema
- the weekly memo can be written without confusion
- the sidecar row can be added without changing the observation core
- the market-reference lane updates without breaking plots
- the system remains comparable to prior manual validation logic

## Practical rule

For the first live window:

- keep the observation core stable
- keep the market lane stable
- record a memo
- record a sidecar row
- avoid redesign during launch

The goal of launch is stability, not expansion.
