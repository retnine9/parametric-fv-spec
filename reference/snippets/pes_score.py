"""
PES entry economics for one candidate.

Inputs:  side_win_p, sweep result, seconds_remaining, min_lockup_floor
Output:  economics dict including primary_score (= duration_adjusted_reward)
"""
from __future__ import annotations

from polymarket_fee import polymarket_fee


def duration_adjusted_reward(
    expected_reward_dollars: float,
    capital_used: float,
    lockup_seconds: float,
    min_lockup_floor: float,
) -> float:
    denom = max(capital_used * lockup_seconds, min_lockup_floor)
    return expected_reward_dollars / denom if denom > 0 else 0.0


def compute_entry_economics(
    side_win_p: float,
    avg_exec: float,
    shares: float,
    notional_used: float,
    seconds_remaining: float,
    min_lockup_floor: float = 1.0,
) -> dict:
    fee_total = polymarket_fee(avg_exec, shares)
    fee_ps = fee_total / shares
    true_breakeven = avg_exec + fee_ps
    expected_reward_per_share = side_win_p - true_breakeven
    expected_reward_dollars = expected_reward_per_share * shares
    dar = duration_adjusted_reward(
        expected_reward_dollars, notional_used, seconds_remaining, min_lockup_floor
    )
    return {
        "true_breakeven": true_breakeven,
        "expected_reward_per_share": expected_reward_per_share,
        "expected_reward_dollars": expected_reward_dollars,
        "reward_per_capital": expected_reward_dollars / notional_used if notional_used > 0 else 0.0,
        "duration_adjusted_reward": dar,
        "primary_score": dar,
    }
