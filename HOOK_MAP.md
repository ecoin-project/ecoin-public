# HOOK_MAP.md

## Purpose

This document defines a hook-based framing layer used alongside the ECOIN weekly observation pipeline.

Where `SCORING.md` defines continuous score dimensions, this file defines a simpler interpretive map of recurring discourse hooks.

These hooks are not direct measurements. They are structural lenses for identifying how discourse captures attention, narrows judgment, creates urgency, or stabilizes belonging.

---

## Core idea

A discourse hook is a recurring framing element that helps pull interpretation in a particular direction.

Hooks do not necessarily determine content by themselves.  
Instead, they shape how content is felt, trusted, amplified, or acted upon.

This map is designed to support:

- framing analysis
- prompt interpretation
- cross-run comparison
- later alignment with ECOIN value-state indicators

---

## The five primary hooks

### 1. Authority

**Definition:**  
A hook that stabilizes belief or action by invoking expertise, legitimacy, hierarchy, institutional trust, or privileged knowledge.

**Typical forms:**
- expert authority
- platform authority
- institutional authority
- technical authority
- hidden or privileged access

**Common cues:**
- "experts say"
- "official guidance"
- "research-backed"
- "data shows"
- "insider knowledge"
- "trusted system"

**What it does:**
- reduces uncertainty by outsourcing judgment
- increases compliance or perceived legitimacy
- shifts evaluation from direct inspection to trust in source

**Related scores:**
- delegated_agency
- superiority_intensity
- fixation_score

---

### 2. Fear

**Definition:**  
A hook that activates attention and action through threat, loss, danger, collapse, exclusion, or future harm.

**Typical forms:**
- threat framing
- collapse framing
- urgency framing
- replacement anxiety
- contamination anxiety
- insecurity framing

**Common cues:**
- "left behind"
- "collapse"
- "unsafe"
- "losing relevance"
- "one emergency away"
- "act before it's too late"

**What it does:**
- compresses attention
- increases readiness to accept solutions
- narrows interpretive openness
- raises demand for rescue, protection, or control

**Related scores:**
- fear_intensity
- urgency_score
- fixation_score
- salvation_promise_score

---

### 3. Chosen-ness / Insider status

**Definition:**  
A hook that creates attraction by promising distinction, elite identity, access, superiority, or membership in a more knowing group.

**Typical forms:**
- insider/outsider division
- elite optimization
- chosen few narrative
- status restoration
- special access promise

**Common cues:**
- "early adopter"
- "ahead of the crowd"
- "insiders understand"
- "top performers"
- "exclusive"
- "most people don’t get this"

**What it does:**
- converts uncertainty into identity advantage
- stabilizes belonging through differentiation
- strengthens attachment by mixing recognition and superiority

**Related scores:**
- superiority_intensity
- polarization_risk
- optimization_promise_score

---

### 4. Prohibition / Closure

**Definition:**  
A hook that narrows the field of possible action or interpretation by emphasizing rules, taboo, danger boundaries, moral sorting, or a single correct path.

**Typical forms:**
- do-not framing
- binary moral sorting
- one-path necessity
- contamination boundary
- closure pressure

**Common cues:**
- "never do this"
- "only this works"
- "if you still believe X, you are naive"
- "this is the only safe path"
- "don’t question"
- "stay away from outsiders"

**What it does:**
- reduces interpretive flexibility
- pushes closure over exploration
- strengthens dependency on approved narratives or systems

**Related scores:**
- fixation_score
- polarization_risk
- delegated_agency

---

### 5. Speed / Pressure

**Definition:**  
A hook that drives action by compressing time, emphasizing immediacy, or making hesitation feel costly.

**Typical forms:**
- urgency to act
- scarcity of time
- timing pressure
- acceleration logic
- now-or-never framing

**Common cues:**
- "now"
- "before it’s too late"
- "don’t wait"
- "act immediately"
- "move fast"
- "timing is everything"

**What it does:**
- reduces deliberation time
- increases impulsive agreement
- amplifies fear and solution uptake
- weakens reflective distance

**Related scores:**
- urgency_score
- fear_intensity
- optimization_promise_score

---

## Secondary hooks

These are not yet treated as primary hooks, but may later become explicit dimensions.

### Shame activation
Frames the audience as already failing, behind, impure, weak, naive, or embarrassing unless they change.

### Rescue / Salvation
Frames a tool, authority, path, or system as a route out of fear, confusion, danger, or instability.

### Purity / Contamination
Frames certain people, ideas, tools, or practices as clean/unclean, safe/unsafe, legitimate/corrupt.

### Enemy construction
Builds coherence by assigning blame, hostility, deception, or contamination to an out-group.

### Optimization promise
Frames life, work, relationships, or identity in terms of strategic self-improvement and performance gain.

---

## How hooks differ from scores

Hooks and scores are related, but not identical.

- **Hooks** are qualitative framing mechanisms.
- **Scores** are quantitative heuristic outputs based on how strongly those mechanisms appear.

A single hook may contribute to multiple scores.  
A single score may be influenced by multiple hooks.

Example:
- Fear may raise `fear_intensity`, `urgency_score`, and `fixation_score`.
- Authority may raise `delegated_agency` and sometimes `superiority_intensity`.
- Chosen-ness may raise `superiority_intensity` and `polarization_risk`.

---

## Approximate hook-to-score mapping

### Authority
- delegated_agency
- fixation_score
- sometimes superiority_intensity

### Fear
- fear_intensity
- urgency_score
- fixation_score
- sometimes salvation_promise_score

### Chosen-ness / Insider status
- superiority_intensity
- polarization_risk
- optimization_promise_score

### Prohibition / Closure
- fixation_score
- polarization_risk
- delegated_agency

### Speed / Pressure
- urgency_score
- fear_intensity
- optimization_promise_score

---

## Use in analysis

This hook map can be used in at least three ways.

### 1. Quick framing pass
Before scoring, identify which hooks dominate the discourse.

### 2. Score interpretation aid
Use hooks to explain why a score is high or low.

### 3. Comparative analysis
Compare outputs not only by score averages but also by dominant hook structure.

Example questions:
- Which hooks are most active this week?
- Did fear rise without authority?
- Did chosen-ness increase while urgency fell?
- Is closure being driven by taboo or by speed pressure?

---

## Methodological caution

These hooks do **not** prove manipulation, deception, or malicious intent by themselves.

A hook is a structural feature, not a moral verdict.

The same hook may appear in:
- benign public communication
- marketing
- ideology
- safety messaging
- activism
- emotional support discourse

Interpretation depends on combination, intensity, repetition, and context.

---

## Relation to ECOIN

In later ECOIN-linked analysis, hooks may help distinguish between:

- exploratory discourse
- closure pressure
- dependency pressure
- symbolic opening
- coercive narrowing
- unstable trust environments

This makes the hook layer useful not only for discourse reading, but also for modeling value-state conditions.

---

## Current status

This hook map is a working conceptual layer.

It is intended for:
- structured interpretation
- documentation consistency
- later comparison across weekly outputs

It is **not yet a validated taxonomy** and may be revised as the observation system evolves.
