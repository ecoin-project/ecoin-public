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

* * *
### 9. preference_pressure_score

Definition:
Strength of pressure pushing discourse toward lower-friction, higher-certainty, more externally guided solutions.

High when:

  * the discourse shifts from reflection to ready-made solutions
  * immediate relief or certainty is preferred over slower understanding
  * external frameworks, experts, or templates become more attractive under pressure

Low when:

  * the discourse preserves self-judgment and tolerance for ambiguity
  * solution preference does not noticeably narrow under emotional pressure

Examples of cues:

  * "I just need the answer now"
  * "give me the exact system"
  * "I do not want to think through all the options"
  * "I need something that tells me what to do"

* * *
### 10. shortcut_risk_score

Definition:
Likelihood that the discourse legitimizes interpretive shortcuts, evidence-skipping, or compressed causal closure under pressure.

High when:

  * a single explanatory frame is accepted too quickly
  * urgency overrides evidence standards
  * automation, gurus, or strong narratives are trusted beyond what the evidence supports
  * enemies or causes are simplified too aggressively

Low when:

  * competing explanations remain visible
  * uncertainty and verification are retained
  * shortcuts are resisted rather than normalized

Examples of cues:

  * "this explains everything"
  * "you do not need to overthink it"
  * "the system already knows"
  * "obviously this is the real cause"

* * *
### 11. emotional_delegation_score

Definition:
Degree to which emotional burden regulation is outsourced alongside judgment, interpretation, or action.

High when:

  * the solution is attractive partly because it removes the need to tolerate fear, confusion, shame, or overload
  * discourse invites emotional surrender to a system, expert, ritual, community, or template
  * reassurance and decision outsourcing are fused

Low when:

  * tools support the user without absorbing emotional responsibility
  * emotional regulation remains primarily human-held

Examples of cues:

  * "let it handle the stress for you"
  * "trust the process and stop worrying"
  * "you do not have to carry this alone because the system decides"

* * *
### 12. pressure_gradient_score

Definition:
Degree to which escalating threat or instability language changes what kinds of solutions become acceptable or desirable.

High when:

  * mild concern escalates into stronger closure or stronger intervention demands
  * rising pressure clearly shifts the discourse toward dependence, rigidity, or salvation promises
  * later-stage framing makes stronger measures feel newly justified

Low when:

  * escalation is weak or absent
  * solution type remains relatively stable across pressure levels

Examples of cues:

  * "at first it was inconvenient, now it feels existential"
  * "what seemed optional is now framed as necessary"
  * "the discourse moves from advice to rescue"

* * *
## Additional run-level sidecar mode scores

These are optional higher-level scores applied to the full output when the emotion-mechanism sidecar is enabled.

### 3. pressure_activation

Definition:
Degree to which the full output captures discourse as pressure-driven rather than merely topic-driven.

High when:

  * multiple items are organized by emotional escalation dynamics
  * functional emotional pressure is repeatedly visible across domains
  * solution-seeking changes track pressure rather than only topic content

Low when:

  * items remain mainly descriptive and topical
  * pressure dynamics are weak or inconsistent

* * *
### 4. closure_pressure

Definition:
Degree to which the output shows emotional pressure converting open uncertainty into narrowed interpretive closure.

High when:

  * ambiguity collapses into single-path solutions across multiple items
  * pressure, urgency, or threat repeatedly compresses interpretive space

Low when:

  * uncertainty remains open
  * pressure does not consistently generate closure

* * *
### 5. emotional_offloading

Definition:
Degree to which the output shows discourse patterns that offload not only cognition but also emotional regulation onto external systems.

High when:

  * reassurance, decision transfer, and relief promises repeatedly co-occur
  * emotional burden transfer is part of solution appeal across multiple items

Low when:

  * external support appears without strong emotional outsourcing

* * *
### 6. shortcut_normalization

Definition:
Degree to which the output shows shortcut reasoning becoming normal, attractive, or socially reinforced under pressure.

High when:

  * evidence-skipping, oversimplification, or pseudo-certainty appears across multiple items
  * shortcut logic is framed as efficient, realistic, or necessary

Low when:

  * shortcuts remain marginal
  * verification and complexity remain visible


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
## Methodological bridge

This scoring framework can be understood as a simplified observational layer within a broader ECOIN-style measurement logic.

In that broader logic:

- **resonance-like conditions** correspond to exploratory openness, structural compatibility, and recoverable interpretive space
- **autonomy-related conditions** correspond to retained human judgment and non-outsourced interpretive capacity
- **lock-in tendencies** correspond to fixation, closure, dependency pressure, and reduced interpretive reversibility
- **pressure-like conditions** may later be modeled as composite discourse states rather than single isolated variables

Within the current weekly observation pipeline, these ideas are used in a deliberately simplified form.

The present system does **not** implement a full state-space, phase-dynamic, or continuous-time formalization.  
Instead, it uses repeatable heuristic score dimensions as a lightweight observational approximation.

This means:

- `exploration` and `expansion` function as partial observational proxies for open and recoverable discourse conditions
- `delegated_agency` functions as a partial proxy for reduced autonomy in interpretive or decision structure
- `fixation_score` and `fixation_proxy` function as partial proxies for lock-in, narrowing, and closure pressure
- future composite measures may extend this logic into more explicit pressure- or circulation-oriented indicators

The purpose of this bridge is not to overclaim formal equivalence, but to clarify that the current scoring system belongs to the same methodological family as broader ECOIN measurement concepts.

In other words, the weekly scoring framework should be read as a **discrete observational approximation**, not as the final formal model.


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


## Related documents

See also:
- [HOOK_MAP.md](HOOK_MAP.md)
