[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18110093.svg)](https://doi.org/10.5281/zenodo.18110093)

# ECOIN Weekly Observation Infrastructure

This repository supports a weekly fixed-prompt observation workflow for analyzing recurring discourse patterns around anxiety, solution-seeking, delegated agency, and fear/superiority framing.

## Current capabilities

- Runs a fixed prompt on a scheduled GitHub Actions workflow
- Saves raw outputs and lightweight text/CSV summaries
- Builds a weekly summary JSON from collected outputs
- Supports a manual sample fallback for testing the aggregation pipeline without live API success
- Maintains external market-reference lanes as contextual comparison series
- Generates normalized comparison artifacts across discourse and market-reference lanes

## Current status

- Workflow structure is operational
- Summary generation is operational
- Manual sample aggregation has been validated
- Market-reference lane generation is operational
- Derived comparison artifacts are operational
- Live API generation is currently limited by billing/quota availability

## Manual batch validation

The manual sample pipeline has been validated across three manual batches:

- `manual_batch_001`
- `manual_batch_002`
- `manual_batch_003`

Each batch currently contains 10 sample JSON files, yielding 50 item-level observations per batch after aggregation.

To switch the active manual batch in GitHub Actions, update:

```yaml
MANUAL_BATCH_ID: "manual_batch_001"
```
in .github/workflows/weekly_observation.yml.

## Output artifacts

Typical outputs include:
- `outputs/raw_YYYYMMDD_xxxxxx.jsonl`
- `outputs/summary_YYYYMMDD_xxxxxx.txt`
- `outputs/summary_YYYYMMDD_xxxxxx.csv`
- `outputs/latest_output.txt`
- `outputs/latest_output.csv`
- `outputs/weekly_summary_<batch_id>.json`
- `outputs/latest_summary.json`
- `outputs/summary_trends.png`
- `outputs/market_reference_trends.png`
- `outputs/market_reference_normalized_trends.png`
- `outputs/combined_normalized_trends.png`
- `outputs/combined_normalized_trends.csv`
- `outputs/alignment_report.json`

This repository currently includes manual sample outputs and a validated aggregation step for generating weekly summary JSON files before live API use.

External reference series such as BTC price may be stored separately from the discourse batches and treated as contextual comparison lanes rather than direct explanatory variables.

External market-reference plots should generally remain separate from discourse-core trend plots in order to preserve scale and interpretive clarity.

At the same time, derived comparison artifacts such as combined normalized overlays and alignment reports may be generated as exploratory cross-lane tools.

These derived artifacts should be treated as provisional and hypothesis-generating rather than as evidence of causation.

## Notes

This repository is intended for structural observation and hypothesis generation, not direct corpus measurement or performance benchmarking.

## Additional derived comparison artifacts

The repository may generate derived comparison artifacts that align external market-reference lanes with discourse-sidecar measurements.

Examples include:
- `outputs/combined_normalized_trends.png`
- `outputs/combined_normalized_trends.csv`
- `outputs/alignment_report.json`

These derived artifacts are exploratory comparison tools.
They are intended for provisional cross-lane reading, not as evidence of causation.

See also:

- [SCORING.md](SCORING.md)
- [HOOK_MAP.md](HOOK_MAP.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [BATCH_COMPARISON.md](BATCH_COMPARISON.md)
- [MARKET_REFERENCE.md](MARKET_REFERENCE.md)
- [API_LAUNCH_CHECKLIST.md](API_LAUNCH_CHECKLIST.md)
