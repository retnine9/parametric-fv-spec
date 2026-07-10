# Prerequisites

This page lists what you need **outside** this repo if you want to run the strategy for real. The case study covers the brain; you supply the body.

## Minimum viable platform

| Capability | Why you need it |
|------------|-----------------|
| Live Up/Down market discovery | The write-up evaluates one market at a time. Something in your stack must list active crypto Up/Down windows (asset, duration, start/end, condition IDs, UP/DOWN token IDs) as new ones roll in. |
| Window open tracking | GBM and OU both need S_0 (spot at window open). You record or reconstruct that per window. |
| Spot feed | Current underlying price (e.g. BTC-USD), fresh enough for vol and momentum. |
| Order book feed | L2 asks (and bids if you do exits) on UP and DOWN. PES sweeps depth for size; the best ask alone is not enough. |
| Clock | Time remaining until window end, in ms or seconds, for GBM scaling and PES lockup scoring. |
| Execution | Taker orders on the prediction market CLOB. PES assumes FOK-style sizing (full fill or reject). |

## Market discovery (the big one)

The hardest prerequisite is **automatic discovery of live Up/Down crypto markets**.

Venues like Polymarket keep spawning short windows. Each one has:

- A title (e.g. "Bitcoin Up or Down, 5 minutes")
- Start and end times
- Two outcome tokens (UP, DOWN)
- A rule: UP wins if spot at end is at or above spot at open

Your system should:

1. Find new markets as they appear (API, indexer, or a list you refresh often)
2. Map each to `(asset, window_duration)` so you load the right parameters
3. Track lifecycle: upcoming, active, near expiry, settled
4. Drop dead or settled markets from the set you evaluate

This repo does not define discovery APIs, slug patterns, or cron jobs. If you cannot auto-find live windows, treat the rest as a research reference.

## What you can still do without discovery

- Read the probability and PES math
- Run the [worked examples](../examples/worked-tick-gbm.md) on synthetic fixtures
- Prototype `evaluate(snapshot)` in a notebook with hand-built inputs
- Backtest if you already store historical snapshots somewhere else

## How the pieces fit together

```
  [Market discovery] -> [Snapshot builder] -> evaluate() -> [Executor]
         ^                      ^                  ^
    you build this          you build this    documented here
```

Only the logic inside `evaluate()` is specified in this case study.
