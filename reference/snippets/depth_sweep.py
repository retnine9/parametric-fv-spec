"""
Depth sweep: fill target USD notional from ask ladder (FOK).

Inputs:  levels [{price, size_shares}, ...] ascending, target_usd
Output:  avg_exec_price, shares, notional_used, or None if insufficient
"""
from __future__ import annotations


def depth_sweep_ask(levels: list[dict], target_usd: float) -> dict | None:
    remaining = target_usd
    cost = 0.0
    shares = 0.0
    for lvl in levels:
        price = float(lvl["price"])
        avail = float(lvl["size_shares"])
        if price <= 0 or avail <= 0:
            continue
        level_notional = price * avail
        if level_notional >= remaining:
            take_shares = remaining / price
            cost += remaining
            shares += take_shares
            remaining = 0.0
            break
        cost += level_notional
        shares += avail
        remaining -= level_notional
    if remaining > 1e-9 or shares <= 0:
        return None
    return {
        "avg_exec_price": cost / shares,
        "shares": shares,
        "notional_used": cost,
    }
