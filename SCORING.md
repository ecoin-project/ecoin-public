# SCORING.md

## Purpose

This document defines the scoring logic used in the ECOIN weekly observation pipeline.

The goal is not to claim objective truth, but to make model-generated observations more stable, comparable, and interpretable across repeated runs.

These scores should be treated as **structured heuristic measures**, not direct measurements of the external world.

---

## General scoring rule

All scores use a **0–100 scale**.

- **0–20**: very weak or nearly absent
- **21–40**: present but limited
- **41–60**: moderate
- **61–80**: strong
- **81–100**: very strong or dominant

Scores should reflect the **intensity of the framing in the output**, not whether the framing is morally good or bad.

---

## Item-level scores

Each item in the observation output may contain the following scores.

### 1. fear_intensity

**Definition:**  
Strength of threat framing, loss framing, collapse framing, urgency, or danger cues.

**High when:**
- imminent loss is emphasized
- decline, collapse, danger, or replacement is foregrounded
- urgency or pressure to act is strong

**Low when:**
- concern is mentioned only mildly
- the item is mainly descriptive without threat pressure

**Examples of cues:**
- "left behind"
- "collapse"
- "unsafe"
- "losing relevance"
- "one emergency away"

---

### 2. superiority_intensity

**Definition:**  
Strength of elite positioning, insider identity, smarter-than-others framing, or status restoration promises.

**High when:**
- the discourse promises advantage over slower, weaker, or less informed others
- insider/outsider distinction is emphasized
- being ahead, superior, optimized, or elite is central

**Low when:**
- solutions are framed neutrally
- no strong status differentiation is present

**Examples of cues:**
- "early adopter"
- "top performers"
- "insider knowledge"
- "more optimized than others"
- "ahead of the crowd"

---

### 3. delegated_agency

**Definition:**  
Degree to which judgment, control, interpretation, or action is outsourced to systems, experts, gurus, templates, or automated tools.

**High when:**
- users are encouraged to rely on tools or authorities rather than their own judgment
- the solution is framed as "let the system decide" or "follow this exact framework"
- managed dependence is part of the promise

**Low when:**
- the discourse encourages direct human judgment
- tools are presented as aids, not replacements for agency

**Examples of cues:**
- "follow this exact system"
- "our tool handles it for you"
- "trust the expert"
- "managed automatically"
- "done for you"

---

### 4. polarization_risk

**Definition:**  
Likelihood that the discourse reinforces binary thinking, in-group/out-group division, scapegoating, moral sorting, or hostile simplification.

**High when:**
- enemies, outsiders, or inferior others are clearly implied
- the discourse pushes strong us/them separation
- moral or cognitive superiority is linked to exclusion

**Low when:**
- the framing remains plural, descriptive, and non-binary
- no clear enemy construction appears

**Examples of cues:**
- "they are blind"
- "most people are sheep"
- "only insiders understand"
- "if you still believe X, you are naive"

---

### 5. urgency_score

**Definition:**  
Strength of immediate action pressure.

**High when:**
- delay is framed as costly or dangerous
- timing pressure is central
- "now or never" logic appears

**Low when:**
- no immediate call to action is implied
- the discourse allows reflection or delay

---

### 6. optimization_promise_score

**Definition:**  
Strength of promises related to efficiency, performance, self-improvement, productivity, or strategic advantage.

**High when:**
- the solution promises sharper, faster, more efficient functioning
- self-optimization is central to the appeal

**Low when:**
- optimization is secondary or absent

---

### 7. salvation_promise_score

**Definition:**  
Strength of rescue, redemption, security, restoration, or relief promises.

**High when:**
- the discourse frames the solution as a way out, rescue route, or path to relief
- emotional or existential safety is part of the promise

**Low when:**
- the solution is practical but not redemptive in tone

---

### 8. fixation_score

**Definition:**  
Degree to which the discourse narrows possibility space and pushes closure, rigidity, dependency, or one-track interpretation.

**High when:**
- a single path is framed as necessary
- complexity is collapsed into one dominant narrative
- exploration is suppressed in favor of closure

**Low when:**
- uncertainty is tolerated
- multiple interpretations remain open
- exploratory framing is preserved

---

## Run-level mode scores

These are higher-level scores applied to the full output, not just one item.

### 1. exploration

**Definition:**  
Degree to which the output preserves openness, plurality, uncertainty tolerance, and pattern-seeking without premature closure.

**High when:**
- multiple interpretations are acknowledged
- caution and nuance remain visible
- the output keeps conceptual space open

**Low when:**
- the output collapses quickly into a single explanatory frame
- interpretive flexibility is weak

---

### 2. expansion

**Definition:**  
Degree to which the output broadens the interpretive field, adds dimensions, or increases conceptual reach.

**High when:**
- the analysis expands beyond surface claims
- broader structural patterns become visible
- the output connects local observations to wider dynamics

**Low when:**
- the output stays narrow, literal, or repetitive

---

## Derived score

### fixation_proxy

A provisional derived measure intended to estimate closure-leaning discourse conditions.

Current formula:

```text
fixation_proxy
= fear_intensity_mean * 0.35
+ delegated_agency_mean * 0.35
+ polarization_risk_mean * 0.20
+ (100 - exploration_mean) * 0.10
```

**Interpretation:**
- higher values suggest stronger closure, dependency, and narrowing pressure
- lower values suggest more exploratory and less coercively fixed discourse conditions

This is a working heuristic and may be revised later.


## Interpretation caution

These scores do **not** directly measure:
- actual public opinion prevalence
- real-world event severity
- psychological diagnosis
- causal truth

They measure the **structure of model-generated discourse observations** under fixed prompt conditions.

---

## Current methodological stance

This scoring system is designed for:
- repeated weekly observation
- comparison across runs
- trend detection
- hypothesis generation
- later connection to ECOIN value-state indicators

It is **not yet a validated psychometric instrument**.

---

## Future extensions

Possible future additions:
- enemy_construction_score
- shame_activation_score
- collapse_narrative_score
- purity_contamination_score
- trust_volatility_score
- symbolic_opening_score
- coercive_closure_score

These should only be added when their definitions can be stated clearly enough for repeated use.
