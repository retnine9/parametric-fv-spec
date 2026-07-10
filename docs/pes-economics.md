# PES economics

**Parametric Economic Selector (PES)** picks trades after `fair_p_up` exists. It scores candidate **actions** on executable economics, not raw probability edge alone.

## Win probabilities

| Side | Probability |
|------|-------------|
| UP | `fair_p_up` |
| DOWN | `1 - fair_p_up` |

## Candidates

For each value in `pes_size_buckets_usd` (e.g. \$10, \$20):

- `ENTER_UP` at that size
- `ENTER_DOWN` at that size

Also `SKIP`, `HOLD`, and position-aware actions when you hold inventory.

## Depth sweep (FOK)

Walk ask levels ascending until you fill `target_usd` or fail:

```text
avg_exec_price = VWAP
shares = notional_used / avg_exec_price
```

No partial fills. If the full notional does not fit in depth, reject with `SKIP_FOK_INSUFFICIENT_ASK_NOTIONAL`.

## Per-candidate math

```text
fee_total      = polymarket_fee(avg_exec_price, shares)
fee_per_share  = fee_total / shares
true_breakeven = avg_exec_price + fee_per_share

expected_reward_per_share  = p_side - true_breakeven
expected_reward_dollars    = expected_reward_per_share * shares
capital_used               = notional_used
reward_per_capital         = expected_reward_dollars / capital_used
lockup_seconds             = seconds_remaining

duration_adjusted_reward   = expected_reward_dollars / max(capital_used * lockup_seconds, min_lockup_floor)
primary_score              = duration_adjusted_reward
```

where $p_{\mathrm{side}}$ is `fair_p_up` for UP and $(1 - p_{\mathrm{up}})$ for DOWN, with $p_{\mathrm{up}} =$ `fair_p_up`.

## Edge multiple (diagnostic)

```text
edge_multiple = expected_reward_per_share / fee_per_share   (if fee_per_share > 0)
```

## Avoid these

- Using best ask as fill price when size > 1 share
- Computing `fee(price, 1) * shares` instead of fee on the full share count
- Treating spread as an extra settlement charge (you already pay the ask / sweep)

## Snippets

- [depth_sweep.py](../reference/snippets/depth_sweep.py)
- [pes_score.py](../reference/snippets/pes_score.py)
