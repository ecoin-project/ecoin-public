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

This repository is organized into four practical lanes:

### 1. Live observation core
The active weekly workflow lives in the fixed-prompt pipeline and its summary artifacts.

This lane is intended for repeated live observation of:
- anxiety patterns
- solution-seeking
- delegated agency
- fear / superiority framing
- pressure-oriented sidecar signals

Primary references:
- `README.md`
- `ARCHITECTURE.md`
- `prompts/fixed_prompt_v2.json`
- `scripts/run_weekly.py`
- `scripts/score_outputs.py`

### 2. Validation and retained legacy references
Manual sample batches and older reference outputs are preserved as validation materials.
They should be treated separately from live weekly runs.

Primary references:
- `samples/`
- `outputs/weekly_summary_manual_batch_001.json`
- `outputs/weekly_summary_manual_batch_002.json`
- `outputs/weekly_summary_manual_batch_003.json`
- `outputs/master_summary_manual_validation.csv`

### 3. Measurement and scoring
Explicit rubrics and sidecar measurement tables live under `measurements/`.
These files translate observed discourse structure into repeatable score dimensions and lightweight comparison fields.

Primary references:
- `SCORING.md`
- `measurements/scoring_rubric.md`
- `measurements/discourse_sidecar.csv`
- `measurements/value_rubric.md`
- `measurements/value_sidecar.csv`

### 4. Method notes and future extensions
Longer-form methodological notes, conceptual interpretation, and future sidecar candidates live under `notes/`.

This lane should include:
- methodological notes about LLM-based observation
- raw longform captures and theory memos
- future sidecar candidates that are not yet part of the active weekly base schema

Primary references:
- `notes/sidecar_summary_design.md`
- `notes/method_note_llm_observation.md`
- `notes/future_sidecar_candidates.md`
- `ARCHITECTURE.md`

### Current live schema status

The current live weekly schema is the pressure-oriented v2 observation core.

It includes:
- the fixed prompt workflow
- weekly summary generation
- sidecar pressure aggregation
- lightweight trend-ready summary outputs

It does **not** yet treat `value_phase_summary` or `response_value_summary` as active weekly base modules.
Those remain future-facing candidates until they prove stable across repeated runs.

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

---

## Experimental Observation Prompt Candidates

This repository includes experimental observation-only prompt candidates under `prompts/candidates/`.

These prompts are not part of the active weekly workflow. They are retained for future validation as possible sidecar modules for observing discourse pressure, self–environment mismatch, affect routing, meaning capture, autonomy, recovery, and lock-in patterns.

These prompts must not be used for diagnosis, ranking, behavioral instruction, settlement decisions, investment advice, or evaluation of individuals.

Current candidate areas include:

- Autonomy / Recovery / Lock-in observation
- Self–Environment Mapping
- Affect Routing
- Meaning Capture Loop detection
- Trust Conversion Mapping
- Value Claim Extraction
- Observation-to-Settlement Boundary Audit

All outputs should be treated as provisional state observations, not judgments or recommendations.
