# Market reference lane

## Purpose

This file documents the role of the external market-reference lane used alongside the weekly discourse observation workflow.

The `data/market_reference.csv` series is not part of the discourse-core observation itself.  
It is a separate contextual lane intended to provide external reference signals that can be compared with discourse patterns over time.

Its function is comparative and hypothesis-generating, not directly explanatory or causal.

## Current assets

The current market-reference lane includes:

- `BTC`  
  Higher-volatility, risk-sensitive reference.  
  Useful as a proxy for speculative attention, expansion pressure, and spike-prone movement.

- `GOLD`  
  Defensive, safe-haven reference.  
  Useful as a proxy for retreat, preservation, and lower-risk positioning.

- `USDJPY`  
  Macro pressure / currency stress / cost-of-living pressure reference.

- `VIX`  
  Volatility / fear / market-stress reference.  
  Useful as a proxy for compression, uncertainty, and overt risk-off conditions.

- `SP500`  
  Broad-market / general risk-appetite reference.  
  Useful as a baseline for overall U.S. equity conditions rather than theme-specific pressure.  

These assets are not treated as direct explanations of discourse shifts.  
They are used as external comparison lanes for reading possible directional or phase relationships.

## Graph roles

The market-reference lane currently produces two graph types:

- `outputs/market_reference_trends.png`  
  Raw-value comparison across assets.  
  This graph is useful for absolute scale and level comparison, but assets with large differences in magnitude may visually compress smaller series.

- `outputs/market_reference_normalized_trends.png`  
  Relative-change comparison, with the first observed point of each asset set to `100`.  
  This graph is useful for comparing directional movement and relative phase behavior across assets without scale distortion.

These two graphs should be read together rather than treated as interchangeable.

## Current data notes

The current `GOLD` series contains mixed-source rows.

The earlier rows:

- `2026-03-01`
- `2026-03-08`
- `2026-03-15`

are currently marked as:

- `manual approximate from tradingeconomics chart`

Later rows such as:

- `2026-03-20`
- `2026-03-21`

are currently marked as:

- `gold_api_free`

with recorded `fetched_at_utc` timestamps.

This means that the current GOLD series is informative, but not yet a fully uniform single-source historical series.  
Interpretation should therefore remain provisional until earlier rows are replaced or confirmed through a more consistent source.

The current `USDJPY` series also contains mixed-source rows.

Earlier rows are currently marked as:

- `manual backfill`

while the latest automated row is marked as:

- `frankfurter_public`

with a recorded `fetched_at_utc` timestamp.

The current `VIX` series is a mix of manual backfill and automated daily-close retrieval.

Earlier rows may be marked as:

- `manual backfill from ^VIX historical prices`

Later automated rows may be marked as:

- `cboe_daily_close_csv`

with a recorded `fetched_at_utc` timestamp.

For `VIX`, weekly observation dates may be mapped to the most recent prior trading-day close when the exact date is not a market session.

This means that the `VIX` lane should be read as a market-stress / volatility reference aligned to the observation window, not necessarily as a same-calendar-day intraday measurement.

The current `SP500` series may begin as a manual backfill and later move to a more regular public daily-close source.

For `SP500`, weekly observation dates may be mapped to the most recent prior trading-day close when the exact date is not a market session.

This means that the `SP500` lane should be read as a broad market baseline aligned to the observation window, not necessarily as a same-calendar-day intraday measurement.

## Current reading

- BTC remains relatively strong.
- GOLD trends downward across the current window.
- USDJPY trends upward, suggesting rising macro/currency pressure.
- VIX rises sharply early and remains elevated relative to baseline, suggesting persistent market stress.
- The market-reference lane currently shows divergence rather than synchronized movement.
  
## Working interpretation

At the current stage, the three main outputs can be read together as follows:

- `summary_trends.png`  
  Represents the discourse layer: a medium-frequency social observation lane, where changes appear more as gradual phase shifts than sharp market-style spikes.

- `market_reference_trends.png`  
  Shows the raw-value structure of external reference assets.  
  In this view, BTC dominates in absolute scale, while GOLD tends to appear closer to a lower baseline.

- `market_reference_normalized_trends.png`  
  Shows relative change rather than absolute size.  
  In the current sample, BTC trends upward while GOLD trends downward, while USDJPY trends upward, suggesting that external reference lanes may move in different directional phases over the same interval.

This makes the market-reference lane useful not only for comparing “high-volatility” versus “low-volatility” behavior, but also for observing cases where assets move in different phase directions during the same period.

## Provisional reading frame

A current working frame is:

- `BTC` = expectation / risk appetite / spike-sensitive movement
- `GOLD` = defense / retreat / safe-haven gravity
- `USDJPY` = macro pressure / currency stress / cost-of-living pressure
- `VIX` = fear / compression / overt market stress
- `SP500` = broad market baseline / general risk appetite / overall equity climate
- `discourse summary` = socially mediated middle layer between external market motion and narrative interpretation

This framing remains exploratory.  
It should be treated as a reading scaffold rather than a final causal model.

## Next possible extensions

Natural next steps include:

- adding additional reference assets such as `SP500`
- creating per-asset market plots
- backfilling GOLD and USDJPY with a more uniform historical source
- comparing discourse shifts with normalized market movement over longer time windows
