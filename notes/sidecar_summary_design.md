# Sidecar Summary Design (v2)

## Purpose

This document describes a non-breaking extension to the current weekly observation summary layer.

The goal is **not** to replace the existing observation core, but to add an experimental sidecar that captures:

- functional emotional pressure
- pressure-linked solution preference
- emotional delegation patterns
- shortcut normalization under pressure

This extension should remain **sidecar-level** until it proves stable across repeated weekly runs.

---

## Design Principle

The current observation core should remain stable.

This sidecar is intended to:

1. preserve compatibility with the current summary structure
2. add pressure-oriented fields without breaking existing downstream outputs
3. remain separable from the core until the measurements are shown to be stable and useful

In other words:

- keep the existing top-level weekly summary readable
- place new detail in a dedicated `sidecar_summary` section
- only promote stable fields into the formal framework later

---

## Methodological Stance

This sidecar does **not** claim to directly measure internal human emotion.

Instead, it estimates **functional pressure signatures visible in discourse**, especially where pressure appears to shape:

- solution preference
- delegation patterns
- closure dynamics
- shortcut acceptance

This is a structured observational heuristic, not a direct psychological measurement.

---

## Scope Extension: Value and Response-Style Sidecars

In addition to pressure-oriented sidecar fields, the sidecar layer may also host two further experimental observational modules:

1. `value_phase_summary`
2. `response_value_summary`

These are not intended to replace the current observation core.
They are sidecar-level extensions meant to track how value and response preference become stabilized around observed discourse patterns.

### A. `value_phase_summary`

This module tracks whether observed solutions, actors, narratives, or platforms appear to gain or lose perceived value through:

- narrative intensity
- attention concentration
- institutional support
- closure pressure
- phase direction

Its purpose is not to assign intrinsic value scores.
Instead, it tracks whether value appears to be:
- story-led
- institution-led
- under-recognized
- over-amplified
- lock-in prone
- freeze prone

This should be treated as a phase-sensitive interpretive sidecar, not as a direct valuation model.

### B. `response_value_summary`

This module tracks which response styles appear to be treated as valuable within the observed discourse environment.

Examples include:
- reassurance
- validation
- challenge
- optimization
- plural-audit

This module also tracks whether the dominant demand appears to lean toward:
- stabilization
- update
- mixed orientation

The aim is not to diagnose users psychologically, but to observe which response forms are repeatedly sought, rewarded, delegated to, and normalized.

### Design rule

Both modules should remain:
- non-breaking
- optional
- explicitly experimental
- separable from the current core
- promotable only after repeated weekly stability is demonstrated

---

## Where This Design Applies

This design is intended for three output artifacts:

1. `weekly_summary_<batch_id>.json`
2. `latest_summary.json`
3. `master_summary.csv`

Recommended usage:

- `weekly_summary_<batch_id>.json`  
  Full sidecar detail

- `latest_summary.json`  
  Lightweight snapshot with only sidecar averages and top proxy labels

- `master_summary.csv`  
  Minimal flat columns for trend tracking

---

## Summary Schema Strategy

### 1. `weekly_summary_<batch_id>.json`

Add a dedicated `sidecar_summary` block while keeping the current summary core intact.

Recommended shape:

```json
{
  "batch_id": "20260403_ab12cd",
  "summary_schema_version": "2.0",
  "question_id": "anxiety_solutions_v2_emotion_sidecar",
  "time_window_assumed": "last_3_to_12_months",

  "n_files": 3,
  "n_items_total": 15,

  "mean_fear_intensity": 68,
  "mean_superiority_intensity": 64,
  "mean_delegated_agency": 72,
  "mean_polarization_risk": 55,
  "mean_exploration": 71,
  "mean_expansion": 58,
  "mean_fixation_proxy": 62.8,

  "top_anxiety_labels": [
    "Economic Instability and Job Security",
    "AI Replacement and Skill Obsolescence",
    "Social Fragmentation and Trust Erosion"
  ],

  "top_solution_modes": [
    "outsourced expertise",
    "automation/monitoring",
    "identity signaling"
  ],

  "sidecar_summary": {
    "enabled": true,

    "mean_preference_pressure_score": 66,
    "mean_shortcut_risk_score": 57,
    "mean_emotional_delegation_score": 63,
    "mean_pressure_gradient_score": 61,

    "mean_pressure_activation": 64,
    "mean_closure_pressure": 60,
    "mean_emotional_offloading": 58,
    "mean_shortcut_normalization": 52,

    "top_functional_emotion_proxies": [
      { "label": "cognitive_overload_escape", "count": 4 },
      { "label": "status_threat", "count": 3 },
      { "label": "uncertainty_intolerance", "count": 3 }
    ],

    "top_delegated_agency_modes": [
      { "label": "diagnostic", "count": 5 },
      { "label": "automated", "count": 4 },
      { "label": "interpretive", "count": 3 }
    ],

    "top_shortcut_risks": [
      { "label": "pseudo_certainty", "count": 4 },
      { "label": "evidence_skipping", "count": 3 },
      { "label": "urgency_override", "count": 3 }
    ],

    "dominant_pressure_mode": "pressure-driven but mixed",
    "pressure_notes": [
      "Solution preference narrows under overload and status threat.",
      "Emotional offloading appears most clearly in expert-led and automated solution bundles."
    ]
  },

  "run_diagnostics": {
    "n_runs_total": 3,
    "n_runs_success": 3,
    "n_runs_error": 0,
    "error_types": {},
    "dominant_mode": "fixation leaning",
    "notes": [
      "Delegated agency remains elevated.",
      "Sidecar fields were present in all runs."
    ]
  },

  "method_notes": [
    "Counts are derived from model-generated observations.",
    "This is not a direct corpus frequency measurement.",
    "Sidecar scores estimate functional pressure signatures visible in discourse, not internal human emotion."
  ]
}
```

---

## 2. latest_summary.json

Keep this lightweight.

Recommended additions:
- sidecar mean scores
- top functional emotion proxies
- dominant_pressure_mode

Recommended shape:

```json
{
  "batch_id": "20260403_ab12cd",
  "time_window_assumed": "last_3_to_12_months",
  "n_files": 3,
  "n_items_total": 15,

  "mean_fear_intensity": 68,
  "mean_superiority_intensity": 64,
  "mean_delegated_agency": 72,
  "mean_polarization_risk": 55,
  "mean_exploration": 71,
  "mean_expansion": 58,
  "mean_fixation_proxy": 62.8,

  "mean_preference_pressure_score": 66,
  "mean_shortcut_risk_score": 57,
  "mean_emotional_delegation_score": 63,
  "mean_pressure_gradient_score": 61,

  "mean_pressure_activation": 64,
  "mean_closure_pressure": 60,
  "mean_emotional_offloading": 58,
  "mean_shortcut_normalization": 52,

  "top_anxiety_labels": [
    "Economic Instability and Job Security",
    "AI Replacement and Skill Obsolescence",
    "Social Fragmentation and Trust Erosion"
  ],

  "top_solution_modes": [
    "outsourced expertise",
    "automation/monitoring",
    "identity signaling"
  ],

  "top_functional_emotion_proxies": [
    "cognitive_overload_escape",
    "status_threat",
    "uncertainty_intolerance"
  ],

  "dominant_mode": "fixation leaning",
  "dominant_pressure_mode": "pressure-driven but mixed",

  "method_notes": [
    "Counts are derived from model-generated observations.",
    "This is not a direct corpus frequency measurement."
  ]
}
```

---

## 3. master_summary.csv

Add flat columns only.

Recommended new columns:

```
mean_preference_pressure_score
mean_shortcut_risk_score
mean_emotional_delegation_score
mean_pressure_gradient_score
mean_pressure_activation
mean_closure_pressure
mean_emotional_offloading
mean_shortcut_normalization
top_functional_emotion_proxy_1
top_functional_emotion_proxy_2
top_functional_emotion_proxy_3
dominant_pressure_mode
```

---

### Aggregation Rules

#### Item-level sidecar means

Use simple averages across all items:
- `mean_preference_pressure_score`
- `mean_shortcut_risk_score`
- `mean_emotional_delegation_score`
- `mean_pressure_gradient_score`

#### Run-level sidecar means

Use simple averages across successful runs:
- `mean_pressure_activation`
- `mean_closure_pressure`
- `mean_emotional_offloading`
- `mean_shortcut_normalization`

Run-level sidecar means are computed from each successful run's `sidecar_mode_scores`, then averaged across runs.

#### Top label counts

Count occurrences across all items:
- `top_functional_emotion_proxies`
- `top_delegated_agency_modes`
- `top_shortcut_risks`

#### Dominant pressure mode

Use a simple threshold rule:

```python
if mean_pressure_activation >= 65 and mean_closure_pressure >= 60:
    dominant_pressure_mode = "pressure-driven and closure-leaning"
elif mean_pressure_activation >= 60:
    dominant_pressure_mode = "pressure-driven but mixed"
elif mean_emotional_offloading >= 60:
    dominant_pressure_mode = "emotionally offloaded"
else:
    dominant_pressure_mode = "mixed / exploratory"
```

#### Pressure notes

Generate 1–2 short rule-based notes only.

Example patterns:
- high overload proxy + high preference pressure
→ “Solution preference narrows under overload.”
- high emotional delegation + high automated or expert-led mode
  → "Emotional offloading appears most clearly in expert-led and automated solution bundles."

#### Missing sidecar handling

If sidecar fields are missing, exclude them from sidecar averages and set `sidecar_summary.enabled` to `false`.

---

### Recommended Output Boundary

To avoid overloading the stable summary layer:

#### Keep at top level

Only stable summary-level averages such as:
- `mean_preference_pressure_score`
- `mean_shortcut_risk_score`
- `mean_emotional_delegation_score`
- `mean_pressure_gradient_score`
- `mean_pressure_activation`
- `mean_closure_pressure`
- `mean_emotional_offloading`
- `mean_shortcut_normalization`
- `dominant_pressure_mode`

#### Keep inside `sidecar_summary`

More detailed or experimental structures such as:
- proxy counts
- delegated mode counts
- shortcut risk counts
- pressure notes
- any future exploratory labels

This keeps the core stable while allowing richer experimentation.

---

### Implementation Guidance

#### Files to change first
1. prompts/fixed_prompt_v2.json
2. scripts/run_weekly.py
3. scripts/score_outputs.py

#### Files to update afterward
4. README.md
5. ARCHITECTURE.md

#### Files not to edit manually
- outputs/*.json
- outputs/*.csv

Those should be regenerated from code.

---

### Minimal Implementation Plan

#### Phase 1

Add fixed_prompt_v2.json and allow prompt switching.

#### Phase 2

Update summary generation logic to support:
- sidecar_summary
- new sidecar mean scores
- CSV sidecar columns

#### Phase 3

Run v1 and v2 side by side for 4–6 weeks.

#### Phase 4

Promote only the stable sidecar fields into the formal framework.

---

## Promotion Criteria

A sidecar field should only be promoted if it shows:
1. repeated interpretability across weeks
2. low confusion or redundancy with existing scores
3. enough distinction from the current observation core
4. usefulness in trend comparison

If a field remains noisy, unstable, or redundant, it should stay in the sidecar layer.

---

## Non-Goals

This sidecar is not intended to:
- replace the current observation core
- claim direct access to human internal states
- function as a clinical or diagnostic framework
- overcomplicate latest_summary.json

Its role is narrower:
- add pressure-oriented observational depth
- remain separable from the main framework
- support safe experimentation before formal adoption

---

## Short Version

The sidecar layer should be treated as:
- detailed in weekly_summary_<batch_id>.json
- lightweight in latest_summary.json
- flat in master_summary.csv
- experimental until proven stable
