[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18110093.svg)](https://doi.org/10.5281/zenodo.18110093)

# ECOIN Weekly Observation Infrastructure

This repository supports a weekly fixed-prompt observation workflow for analyzing recurring discourse patterns around anxiety, solution-seeking, delegated agency, and fear/superiority framing.

## Current capabilities

- Runs a fixed prompt on a scheduled GitHub Actions workflow
- Saves raw outputs and lightweight text/CSV summaries
- Builds a weekly summary JSON from collected outputs
- Preserves manual sample batches for aggregation and scoring validation
- Maintains external market-reference lanes as contextual comparison series
- Generates normalized comparison artifacts across discourse and market-reference lanes

## Current status

- Workflow structure is operational
- Live API-backed weekly generation is operational
- Summary generation is operational
- Manual batch validation has been preserved as a separate validation reference
- Market-reference lane generation is operational
- Derived comparison artifacts are operational

## Manual batch validation

The manual sample pipeline was validated across three manual batches:

- `manual_batch_001`
- `manual_batch_002`
- `manual_batch_003`

Each batch contains 10 sample JSON files, yielding 50 item-level observations per batch after aggregation.

These manual batches are retained as validation references and should be treated separately from live weekly runs.

## Output artifacts

Typical live outputs include:

- `outputs/raw_YYYYMMDD_xxxxxx.jsonl`
- `outputs/summary_YYYYMMDD_xxxxxx.txt`
- `outputs/summary_YYYYMMDD_xxxxxx.csv`
- `outputs/latest_output.txt`
- `outputs/latest_output.csv`
- `outputs/weekly_summary_<batch_id>.json`
- `outputs/latest_summary.json`
- `outputs/master_summary.csv`
- `outputs/summary_trends.png`
- `outputs/market_reference_trends.png`
- `outputs/market_reference_normalized_trends.png`
- `outputs/combined_normalized_trends.png`
- `outputs/combined_normalized_trends.csv`
- `outputs/alignment_report.json`

Retained manual validation outputs may include:

- `outputs/weekly_summary_manual_batch_001.json`
- `outputs/weekly_summary_manual_batch_002.json`
- `outputs/weekly_summary_manual_batch_003.json`
- `outputs/master_summary_manual_validation.csv`

External reference series such as BTC price may be stored separately from the discourse batches and treated as contextual comparison lanes rather than direct explanatory variables.

External market-reference plots should generally remain separate from discourse-core trend plots in order to preserve scale and interpretive clarity.

At the same time, derived comparison artifacts such as combined normalized overlays and alignment reports may be generated as exploratory cross-lane tools.

These derived artifacts should be treated as provisional and hypothesis-generating rather than as evidence of causation.

## Notes

This repository is intended for structural observation and hypothesis generation, not direct corpus measurement or performance benchmarking.

## Documentation map

This repository is organized into four practical layers:

### 1. Observation core
The stable weekly observation workflow lives in the fixed-prompt pipeline and its summary artifacts.
This layer is intended for repeated structural observation of anxiety, solution-seeking, delegated agency, and fear/superiority framing.

Primary references:
- `README.md`
- `ARCHITECTURE.md`
- `prompts/fixed_prompt.json`

### 2. Measurement and scoring
Explicit rubrics and sidecar measurement tables live under `measurements/`.
These files translate observed discourse structure into repeatable score dimensions and lightweight comparison fields.

Primary references:
- `SCORING.md`
- `measurements/scoring_rubric.md`
- `measurements/discourse_sidecar.csv`
- `measurements/value_rubric.md`
- `measurements/value_sidecar.csv`

### 3. Experimental sidecar extensions
Non-breaking extensions to the weekly summary schema are designed and documented in `notes/`.
These additions remain sidecar-level until they prove stable across repeated runs.

Primary references:
- `notes/sidecar_summary_design.md`

### 4. Higher-level interpretation and connection
Longer-range conceptual connections, value-state interpretation, and external comparison lanes belong to the broader architecture and reference documents.
These should be treated as exploratory and hypothesis-generating rather than as direct causal explanation.

Primary references:
- `ARCHITECTURE.md`
- `MARKET_REFERENCE.md`
- `BATCH_COMPARISON.md`

### Current extension direction
The current extension direction adds two experimental sidecar families:
- `value_phase_summary`: tracks value stabilization signals such as narrative intensity, attention concentration, institutional support, closure pressure, and phase direction
- `response_value_summary`: tracks which response styles are being valued, sought, delegated to, and reinforced

These extensions are intended to remain compatible with the current weekly observation core.

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
