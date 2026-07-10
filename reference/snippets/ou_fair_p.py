"""
OU mean-reversion probability mr_p.

Inputs:  spot, window_open, sigma (annualized), time_remaining_ms, ou_theta, ou_mu
Output:  mr_p
Units:   tau in seconds for OU; sigma annualized
"""
from __future__ import annotations

import math

SECONDS_PER_YEAR = 31_557_600.0


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def ou_mr_p(
    spot: float,
    window_open: float,
    sigma: float,
    time_remaining_ms: int,
    theta: float,
    mu: float = 0.0,
) -> float:
    if spot <= 0 or window_open <= 0 or time_remaining_ms <= 0:
        raise ValueError("invalid inputs")
    x = math.log(spot / window_open)
    safe_theta = max(theta, 1e-6)
    tau = time_remaining_ms / 1000.0
    exp_neg = math.exp(-safe_theta * tau)
    e_x = mu + (x - mu) * exp_neg
    sigma_per_sec = sigma / math.sqrt(SECONDS_PER_YEAR)
    v_x = (sigma_per_sec**2 / (2.0 * safe_theta)) * (1.0 - math.exp(-2.0 * safe_theta * tau))
    if v_x < 1e-24:
        if e_x > 0:
            return 0.99
        if e_x < 0:
            return 0.01
        return 0.50
    z = e_x / math.sqrt(v_x)
    return max(0.01, min(0.99, norm_cdf(z)))
