[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18110093.svg)](https://doi.org/10.5281/zenodo.18110093)

# ECOIN Weekly Observation Infrastructure

This repository supports a weekly fixed-prompt observation workflow for analyzing recurring discourse patterns around anxiety, solution-seeking, delegated agency, and fear/superiority framing.

## Current capabilities

- Runs a fixed prompt on a scheduled GitHub Actions workflow
- Saves raw outputs and lightweight text/CSV summaries
- Builds a weekly summary JSON from collected outputs
- Supports a manual sample fallback for testing the aggregation pipeline without live API success

## Current status

- Workflow structure is operational
- Summary generation is operational
- Manual sample aggregation has been validated
- Live API generation is currently limited by billing/quota availability

## Output artifacts

Typical outputs include:

- `raw_YYYYMMDD_xxxxxx.jsonl`
- `summary_YYYYMMDD_xxxxxx.txt`
- `summary_YYYYMMDD_xxxxxx.csv`
- `latest_output.txt`
- `latest_output.csv`
- `weekly_summary_<batch_id>.json`
- `latest_summary.json`

This repository currently includes manual sample outputs and a validated aggregation step for generating weekly summary JSON files before live API use.

## Notes

This repository is intended for structural observation and hypothesis generation, not direct corpus measurement or performance benchmarking.

See also:
- [SCORING.md](SCORING.md)
- [HOOK_MAP.md](HOOK_MAP.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
