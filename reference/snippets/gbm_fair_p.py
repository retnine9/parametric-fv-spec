"""
GBM mean-reversion probability mr_p = P(finish UP).

Inputs:  spot, window_open, sigma (annualized), time_remaining_ms
Output:  mr_p in [0.01, 0.99]
Units:   t converted to years; sigma annualized
"""
from __future__ import annotations

import math

SECONDS_PER_YEAR = 31_557_600.0


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def gbm_mr_p(
    spot: float,
    window_open: float,
    sigma: float,
    time_remaining_ms: int,
) -> float:
    t_years = (time_remaining_ms / 1000.0) / SECONDS_PER_YEAR
    if t_years <= 0 or spot <= 0 or window_open <= 0:
        raise ValueError("invalid inputs")
    x = math.log(spot / window_open)
    denom = sigma * math.sqrt(t_years)
    if denom < 1e-12:
        if x > 0:
            return 0.99
        if x < 0:
            return 0.01
        return 0.50
    d = x / denom
    return max(0.01, min(0.99, norm_cdf(d)))
