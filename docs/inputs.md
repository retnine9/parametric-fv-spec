# Input contract

Treat the strategy as a pure function. Your platform passes a **MarketSnapshot** whenever you want a decision.

## MarketSnapshot fields

| Field | Type | Description |
|-------|------|-------------|
| `spot` | float | Underlying price S > 0 |
| `window_open` | float | Open/strike S_0 > 0 |
| `time_remaining_ms` | int | Ms until window end |
| `window_duration_ms` | int | Full window length (legacy edge path only) |
| `ask_up` | float | Best ask UP (diagnostics; PES uses depth) |
| `ask_down` | float | Best ask DOWN, or 0 if unknown |
| `has_real_down` | bool | True if DOWN book is real (not synthetic `1 - ask_up`) |
| `ask_levels_up` | list | `[{price, size_shares}, ...]` ascending |
| `ask_levels_down` | list | Same for DOWN |
| `quote_age_up_ms` | int | UP book age |
| `quote_age_down_ms` | int | DOWN book age |
| `spread_up` | float | Optional, for spread gate |
| `spread_down` | float | Optional, for spread gate |
| `seconds_remaining` | float | `time_remaining_ms / 1000` |

## StrategyState (carries across ticks)

| Field | Description |
|-------|-------------|
| `vol_estimator` | Rolling prices for sigma |
| `momentum_prices` | Buffer for momentum lookback |
| `rolling_up_rate` | Optional, for blend / adaptive mu |
| `position` | Flat, long UP/DOWN, cooldown |
| `last_trade_ms` | Cooldown gate |

## Params

One bundle per `(asset, window_duration)`. See [parameters.md](parameters.md).

## Spot tick stream

Push `(timestamp_ms, spot)` on each update:

- At least 5 seconds between stored samples (drop closer ticks)
- Drop invalid prices (non-finite or <= 0)

## Skip PES when

- VolEstimator not ready (fewer than 20 spaced samples or fewer than 5 returns)
- Missing spot or open, or zero time remaining
- DOWN entry requested but `has_real_down` is false

## Example decision JSON

```json
{
  "action": "ENTER_UP",
  "side": "UP",
  "size_usd": 20.0,
  "fair_p_up": 0.58,
  "primary_score": 0.00042,
  "reason_code": "SELECTED",
  "components": {
    "mr_p": 0.55,
    "momentum_p": 0.62,
    "blended_p": 0.57,
    "sigma": 0.65
  }
}
```

Extra telemetry fields are up to you. `reason_code` values should match [pes-gates.md](pes-gates.md).
