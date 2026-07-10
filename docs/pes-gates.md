# PES gates

Gates run after economics. A failed gate blocks that candidate.

## Typical order

| Gate | Reason code | Summary |
|------|-------------|---------|
| depth_fok | `SKIP_FOK_INSUFFICIENT_ASK_NOTIONAL` | Full notional must fill |
| min_reward | `SKIP_MIN_REWARD` | Expected reward dollars too low |
| spread | `SKIP_WIDE_SPREAD` | Both spreads above max (AND logic) |
| quote_age | `SKIP_QUOTE_AGE` | Book too stale |
| pin_risk | `SKIP_PIN_RISK` | Near strike late in window |
| jump_quarantine | `SKIP_JUMP_QUARANTINE` | Recent jump vs short sigma |
| stop_before_end | `SKIP_STOP_BEFORE_END` | Too close to expiry |
| capital | `SKIP_CAPITAL` | Capital or exposure cap |
| cooldown | `SKIP_COOLDOWN` | Still in cooldown |
| flow_toxicity | `SKIP_FLOW_TOXICITY` | PM flow vs spot disagree |
| calibration_guard | `SKIP_CALIBRATION_GUARD` | Calibration sanity |
| cheap_token | `SKIP_CHEAP_TOKEN` | Cheap ask; stricter reward rules |

## Scorer checks (after gates)

| Check | Reason code |
|-------|-------------|
| `primary_score <= score_threshold` | `SKIP_SCORE_BELOW_THRESHOLD` |
| `expected_reward_dollars <= min` | `SKIP_MIN_EXPECTED_REWARD_DOLLARS` |
| `expected_reward_per_share <= min` | `SKIP_MIN_EXPECTED_REWARD_PER_SHARE` |

Each gate can be toggled with `*_enabled` config flags.

## Spread gate

Block only when **both** sides are wide:

```text
block = (spread_up > max_spread) AND (spread_down > max_spread)
```

`max_spread` is often 0.40.

## Snippet

Full gate orchestration is verbose; [pes_score.py](../reference/snippets/pes_score.py) covers economics and threshold checks.
