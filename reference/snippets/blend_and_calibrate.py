"""
Momentum, trend boost, blend, and calibration → fair_p_up.

Inputs:  mr_p, momentum_p, sigma, params dict
Output:  blended_p, fair_p_up
"""
from __future__ import annotations

import math


def smooth_ramp(value: float, start: float, full: float) -> float:
    if full <= start:
        return 0.0
    return max(0.0, min(1.0, (value - start) / (full - start)))


def blend_and_calibrate(
    mr_p: float,
    momentum_p: float,
    sigma: float,
    d_abs: float,
    rolling_up_rate: float | None,
    *,
    momentum_blend_floor: float,
    momentum_blend_ceiling: float,
    momentum_blend_max: float,
    trend_boost_max: float,
    trend_ramp_start: float,
    trend_ramp_full: float,
    persistence_base_rate: float,
    persistence_ramp_start: float,
    persistence_ramp_full: float,
    cal_scale: float = 1.0,
    cal_drift: float = 0.0,
    cal_drift_sigma: float = 0.0,
    isotonic_x: list[float] | None = None,
    isotonic_y: list[float] | None = None,
) -> tuple[float, float]:
    layer1 = smooth_ramp(d_abs, trend_ramp_start, trend_ramp_full)
    layer2 = 0.0
    if rolling_up_rate is not None and rolling_up_rate >= 0:
        dev = abs(rolling_up_rate - persistence_base_rate)
        layer2 = smooth_ramp(dev, persistence_ramp_start, persistence_ramp_full)
    trend_factor = max(layer1, layer2)
    eff_max = momentum_blend_max + (1.0 - momentum_blend_max) * trend_factor * trend_boost_max

    if momentum_blend_ceiling <= momentum_blend_floor or eff_max <= 0:
        blend_w = 0.0
    else:
        blend_w = max(0.0, min(1.0, (sigma - momentum_blend_floor) / (momentum_blend_ceiling - momentum_blend_floor)))
        blend_w *= eff_max

    blended_p = (1.0 - blend_w) * mr_p + blend_w * momentum_p

    if isotonic_x and isotonic_y and len(isotonic_x) == len(isotonic_y) and len(isotonic_x) > 0:
        # linear interp
        xp, fp = isotonic_x, isotonic_y
        if blended_p <= xp[0]:
            fair_p = fp[0]
        elif blended_p >= xp[-1]:
            fair_p = fp[-1]
        else:
            fair_p = fp[-1]
            for i in range(len(xp) - 1):
                if xp[i] <= blended_p <= xp[i + 1]:
                    t = (blended_p - xp[i]) / (xp[i + 1] - xp[i])
                    fair_p = fp[i] + t * (fp[i + 1] - fp[i])
                    break
        fair_p_up = max(0.01, min(0.99, fair_p))
    else:
        drift = cal_drift + cal_drift_sigma * sigma
        fair_p_up = max(0.01, min(0.99, 0.5 + (blended_p - 0.5) * cal_scale + drift))

    return blended_p, fair_p_up
