# Future Sidecar Candidates

## Purpose

This note records candidate extensions that may later be added to the weekly observation framework.

These are **not** part of the current pressure-oriented v2 base design.
They are documented separately in order to keep the current specification stable.

The current base sidecar remains focused on:
- functional emotional pressure
- pressure-linked preference shifts
- emotional delegation
- shortcut normalization
- pressure gradients

The modules below are future-facing candidates only.

---

## Candidate A: `value_phase_summary`

### Idea

Some solutions, actors, products, institutions, or narratives do not merely appear in discourse.
They also gain or lose **perceived value** through:
- narrative intensity
- attention concentration
- institutional support
- closure pressure

This candidate module is intended to track whether a target appears:
- over-amplified
- under-recognized
- lock-in prone
- freeze prone
- institution-led
- story-led

### Possible minimal structure

```json
{
  "value_phase_summary": {
    "enabled": true,
    "status": "experimental",
    "global_signals": {
      "dominant_value_pattern": "",
      "dominant_phase_direction": "expansion | contraction | mixed",
      "overall_closure_pressure": "low | medium | high"
    },
    "value_patterns": [
      {
        "target": "",
        "target_type": "solution | product | person | institution | narrative | platform | identity_signal",
        "phase_direction": "expansion | contraction | mixed",
        "narrative_intensity": "low | medium | high",
        "attention_concentration": "low | medium | high",
        "institutional_support": "low | medium | high",
        "closure_pressure": "low | medium | high",
        "value_reading": "story_led | institution_led | under_recognized | over_amplified | lock_in_risk | freeze_risk | mixed",
        "signal_basis": [""],
        "stability_note": "",
        "confidence": "low | medium | high"
      }
    ],
    "interpretation_note": "",
    "promotion_candidate": false
  }
}
```

### Why it is not base v2 yet

- it adds a more interpretive layer than the current pressure sidecar
- it risks mixing value theory with direct weekly observation too early
- it needs repeated use before schema promotion

---

## Candidate B: `response_value_summary`

### Idea

People do not only seek answers.
They also assign value to **response styles**.

Different conditions may increase demand for:
- reassurance
- validation
- challenge
- optimization
- plural audit
- authority-backed correction

This candidate module is meant to track what kinds of response modes are currently being valued.

### Possible minimal structure

```json
{
  "response_value_summary": {
    "enabled": true,
    "status": "experimental",
    "global_signals": {
      "dominant_feedback_demand": "reassurance | validation | challenge | optimization | plural_audit | mixed",
      "dominant_update_orientation": "stabilize | update | mixed",
      "alignment_pressure": "low | medium | high",
      "challenge_tolerance": "low | medium | high"
    },
    "response_modes": [
      {
        "mode": "reassurance | validation | challenge | optimization | plural_audit",
        "observed_value_basis": [""],
        "delegation_form": "comfort | correction | decision | optimization | perspective_diversification",
        "risk": "echo_reinforcement | dependency | shame_escalation | premature_closure | fragmentation",
        "signal_basis": [""],
        "confidence": "low | medium | high"
      }
    ],
    "interpretation_note": "",
    "promotion_candidate": false
  }
}
```

### Why it is not base v2 yet

- it expands from pressure observation into response-style valuation
- it needs a clearer rubric before weekly integration
- it should first be tested as a separate sidecar track

---

## Candidate C: Value Field / Phase Framing

### Idea

A broader theoretical layer may later connect:
- value formation
- narrative convergence
- attention concentration
- institutional reinforcement
- lock-in and freeze dynamics

This framing is useful for:
- monthly synthesis
- theory memos
- interpretation of longer-term shifts

But it is too heavy to become part of the current weekly base schema.

---

## Placement Rule

For now, these candidates should:
- remain outside the current base sidecar schema
- be documented as optional experimental extensions
- stay separate from `latest_summary.json`
- stay separate from `master_summary.csv`
- be introduced into weekly outputs only after repeated stability testing

---

## Promotion Criteria

A future sidecar candidate should only be promoted if it shows:
1. repeated interpretability across weeks
2. low schema friction
3. clear distinction from existing pressure-oriented fields
4. enough practical value to justify ongoing maintenance

If not, it should remain a note-level or monthly-synthesis construct.

---

## Short Version

These modules are promising, but not yet base v2.

For now:
- pressure-oriented sidecar remains the active weekly design
- value-phase and response-value remain candidate extensions
- broader phase/value theory should stay in notes or monthly synthesis
