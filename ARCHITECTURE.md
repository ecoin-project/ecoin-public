# ARCHITECTURE.md

## Purpose

This document outlines the conceptual architecture of the ECOIN weekly observation infrastructure.

The current system should not be understood as a finished product, but as a structured observation core that can later be extended into a broader research and analysis framework.

---

## Overview

The long-term direction is to organize the system into four layers:

1. Observation layer
2. Measurement layer
3. Time-series layer
4. Connection layer

The current fixed-prompt workflow mainly functions as the first layer: an observation core.

---

## Layer 1: Observation layer

This layer is already partially implemented.

Its role is to make discourse patterns observable in a stable and comparable format.  
Typical outputs include:

- anxiety labels
- amplifying signals
- solutions sought
- delegated agency mechanisms
- fear / superiority framing
- exploration / expansion mode scores

This layer does not yet claim direct measurement of the external world.  
Its purpose is to create a repeatable structure for observation.

---

## Layer 2: Measurement layer

The next step is to translate observed discourse structure into more explicit score dimensions.

Examples include:

- fear intensity
- superiority intensity
- delegated agency intensity
- exploration score
- expansion score
- fixation / closure score
- urgency score

The main requirement at this layer is not merely adding score fields, but defining them clearly enough to support repeated use and comparison.

This is the layer that makes the system more research-oriented.

---

## Layer 3: Time-series layer

After repeated outputs accumulate, the system can move from single-run observation to week-by-week comparison.

This layer is intended to support:

- weekly aggregation
- trend comparison
- change detection across runs
- dominant discourse shifts over time

Typical questions at this layer include:

- When does fear intensity rise?
- When does exploration fall while fixation rises?
- Which solution patterns become dominant across weeks?

This is the layer where repeated observation becomes longitudinal structure.

---

## Layer 4: Connection layer

The final layer connects the observation system to broader interpretive frameworks.

Potential future directions include:

- connection to research on fear/superiority framing
- connection to ECOIN value-state indicators
- connection to external weekly indicators or market data

These connections should be treated cautiously and as hypothesis-generating rather than as direct causal claims.

---

## Practical build order

A practical development sequence is:

1. Stabilize the observation format
2. Generate weekly summary outputs
3. Define scoring logic explicitly
4. Add lexical / framing extraction layers
5. Compare time-series outputs
6. Explore external connections

---

## Long-term vision

The long-term aim is to treat this system not as a prompt experiment, but as a discourse-climate observation framework.

In that form, it may support structured observation of:

- recurring social anxieties
- dominant solution modes
- pressure toward delegation or closure
- exploratory versus fixed discourse conditions
- shifts in framing across time

The most important principle is that the current fixed prompt should be treated as an observation core, not as the final form of the system.
