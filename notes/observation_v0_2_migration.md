# ECOIN Observation v0.2 Migration Note

## Purpose

This note documents the migration path from the current weekly observation workflow to ECOIN Observation v0.2.

The migration is intentionally additive. It preserves existing prompt fields, historical outputs, trend files, and scheduled workflow behavior until explicit activation.

## Migration rules

1. Keep all existing fields unchanged.
2. Keep historical data unchanged.
3. Treat sidecar and v0.2 transition fields as optional during migration.
4. Validate with warnings and continue; do not fail scheduled runs because optional fields are absent.
5. Do not activate `fixed_prompt_v0_2.json` in GitHub Actions until a later explicit activation request.

## v0.2 additions

### Schema and prompt metadata

v0.2 observations may declare:

- `observation_schema_version: "0.2"`
- an `observation_scope` block identifying outputs as model-generated discourse observations rather than direct corpus, diagnostic, or personality measurements

### Transition indicators

v0.2 adds optional item-level transition indicators:

- `pause_capacity`
- `counterfactual_tolerance`
- `integration_score`
- `meaning_concentration`
- `recovery_potential`

These use the existing 0-100 observational scale and are not diagnostic measures.

### Functional process map

v0.2 adds an optional `functional_process_map` using neutral process terms:

- `divergence`
- `convergence`
- `structuring`
- `implementation`
- `memory_reference`
- `field_response`
- `social_binding`
- `value_charge`

These are descriptive process terms, not personality or metaphysical measurements.

## Prohibited direct measurement fields

MBTI, Big Five, tarot, and sephirot must not be used as direct measured fields, diagnostic labels, scoring targets, or required output dimensions.

They may appear only in documentation as optional interpretive translation layers, with caveats that ECOIN Observation does not measure them directly.

## Safe implementation order

1. Add `schemas/observation_v0_2.json`.
2. Add `prompts/fixed_prompt_v0_2.json`.
3. Add warning-only validation and schema-version metadata to `scripts/score_outputs.py`.
4. Add optional raw-row run metadata to `scripts/run_weekly.py`.
5. Update architecture, scoring, and README documentation.
6. Keep `.github/workflows/weekly_observation.yml` unchanged.
7. Validate manually before any later workflow activation.

## Compatibility stance

Unversioned observations should be treated as legacy-compatible. Missing v0.2 optional fields should generate diagnostics, not failure.
