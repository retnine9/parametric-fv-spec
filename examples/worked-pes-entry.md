# Worked example: PES entry

Assume `fair_p_up = 0.58`. Two size buckets, two sides.

## UP asks

| Price | Size (shares) |
|-------|----------------|
| 0.52 | 100 |
| 0.54 | 200 |

## DOWN asks

| Price | Size (shares) |
|-------|----------------|
| 0.46 | 150 |
| 0.48 | 200 |

`seconds_remaining = 120`, `min_lockup_floor = 1.0`, buckets = [$10, $20].

## ENTER_UP \$10

Sweep \$10 on UP asks at 0.52:

```text
shares = 10 / 0.52 = 19.23
fee_total = polymarket_fee(0.52, 19.23) = 0.1560
fee_per_share = 0.1560 / 19.23 = 0.00811
true_breakeven = 0.52 + 0.00811 = 0.52811
expected_reward_per_share = 0.58 - 0.52811 = 0.05189
expected_reward_dollars = 0.05189 * 19.23 = 0.998
duration_adjusted_reward = 0.998 / max(10 * 120, 1) = 0.000832
```

## ENTER_DOWN \$10

Win prob on DOWN: $p_{\mathrm{down}} = 1 - 0.58 = 0.42$.

If true breakeven on a DOWN sweep at 0.46 is above 0.42, expected reward is negative and gates should fail.

## Selection

Compare `primary_score` across viable candidates. Highest above `pes_score_threshold` wins (here, likely UP \$10 with `reason_code = SELECTED`).

## Common mistakes

- Pricing \$20 at the 0.52 best ask without walking the book
- Using `fee(0.52, 1) * shares` instead of `polymarket_fee(avg_exec, shares)`
- Comparing raw edge at top of book instead of PES economics

Fixture: [fixtures/depth_book.json](fixtures/depth_book.json)
