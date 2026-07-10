# Strategy boundary

What this case study gives you versus what you build yourself.

## Provided here

| Piece | Doc |
|-------|-----|
| P(UP) from vol, moneyness, momentum | [gbm-engine.md](gbm-engine.md), [ou-engine.md](ou-engine.md), [momentum-and-blend.md](momentum-and-blend.md) |
| Realized vol estimator | [vol-estimator.md](vol-estimator.md) |
| Calibration to `fair_p_up` | [calibration.md](calibration.md) |
| Taker fee formula | [fees.md](fees.md) |
| PES economics, gates, selection | [pes-economics.md](pes-economics.md), [pes-gates.md](pes-gates.md), [pes-selection.md](pes-selection.md) |
| Parameter schema | [parameters.md](parameters.md), [schema/params.schema.json](../schema/params.schema.json) |
| Worked examples | [examples/](../examples/) |

## You build

| Piece | Notes |
|-------|-------|
| Live Up/Down market discovery | Required for production. See [prerequisites.md](prerequisites.md). |
| Spot feed | Exchange WebSocket, index, etc. |
| Order book feed | L2 on UP and DOWN |
| Window open tracking | S_0 per active window |
| `evaluate()` wiring | Vol, then probability, then PES, on each tick |
| Order execution | CLOB client, FOK/IOC behavior |
| Capital and risk | Limits, bankroll, multi-market allocation |
| Backtest harness | If you want history |
| Logging and ops | Your choice |

## Pure function shape

```text
Decision = evaluate(snapshot: MarketSnapshot, state: StrategyState, params: Params)
```

Input: everything needed for one market at one instant.  
Output: action, size, scores, reason codes.  
The spec itself has no side effects (no orders, no network calls).

## Ways people use this

**Research:** Run fixtures through the snippets and check against the worked examples.

**Live:** discovery, build snapshot, `evaluate()`, send order. Only the middle step is documented here.

**Backtest:** Replay stored snapshots; your simulator handles fills and PnL.

## Out of scope

- Production bot source code
- Picking which assets to trade beyond "you chose a market"
- Spread capture, end-of-window rules, market making, ML pipelines
- GARCH for pricing vol
- Optimizers, shadow replays, parity audit tooling
