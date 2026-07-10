"""
Polymarket taker fee: round after shares * rate.

Inputs:  price (per share), shares (count)
Output:  fee_total (USD)
"""
from __future__ import annotations


def polymarket_fee(price: float, shares: float = 1.0) -> float:
    p = max(0.01, min(0.99, price))
    q = p * (1.0 - p)
    raw = shares * p * 0.25 * (q * q)
    rounded = round(raw, 4)
    if rounded > 0:
        return max(rounded, 0.0001)
    return 0.0


def fee_per_share(price: float, shares: float) -> float:
    total = polymarket_fee(price, shares)
    return total / shares if shares > 0 else 0.0
