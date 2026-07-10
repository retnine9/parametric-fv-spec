"""
VolEstimator: non-GARCH pricing volatility.

Inputs:  price ticks (timestamp_ms, spot), params vol_window_secs, vol_floor, vol_ceiling
Output:  annualized sigma (float), ready (bool)
Units:   sigma annualized; timestamps ms; min 5s between samples
"""
from __future__ import annotations

import math
from collections import deque

SECONDS_PER_YEAR = 31_557_600.0
EMA_ALPHA = 0.3


class VolEstimator:
    def __init__(self, window_secs: int, floor: float, ceiling: float):
        self.window_secs = window_secs
        self.floor = floor
        self.ceiling = ceiling
        self.prices: deque[tuple[int, float]] = deque()
        self.returns: deque[float] = deque()
        self.ret_sum = 0.0
        self.ret_sum_sq = 0.0
        self.current_sigma = floor
        self.vol_is_computed = False

    def push_price(self, ts_ms: int, price: float) -> None:
        if not math.isfinite(price) or price <= 0:
            return
        if self.prices and ts_ms - self.prices[-1][0] < 5000:
            return
        prev = self.prices[-1] if self.prices else None
        self.prices.append((ts_ms, price))
        if prev is not None:
            prev_ts, prev_price = prev
            dt = (ts_ms - prev_ts) / 1000.0
            if prev_price > 0 and 5.0 <= dt < 120.0:
                lr = math.log(price / prev_price) / math.sqrt(dt)
                self.returns.append(lr)
                self.ret_sum += lr
                self.ret_sum_sq += lr * lr
        self._evict(ts_ms)
        self._recompute()

    def _evict(self, now_ms: int) -> None:
        cutoff = now_ms - self.window_secs * 1000
        while self.prices and self.prices[0][0] < cutoff:
            self.prices.popleft()
            if self.returns:
                r = self.returns.popleft()
                self.ret_sum -= r
                self.ret_sum_sq -= r * r

    def _recompute(self) -> None:
        n = len(self.returns)
        if n < 5:
            self.current_sigma = self.floor
            self.vol_is_computed = False
            return
        nf = float(n)
        mean = self.ret_sum / nf
        variance = (self.ret_sum_sq / (nf - 1.0)) - (mean * mean * nf / (nf - 1.0))
        sigma_per_sec = math.sqrt(max(variance, 0.0))
        raw = sigma_per_sec * math.sqrt(SECONDS_PER_YEAR)
        raw = max(self.floor, min(self.ceiling, raw))
        if self.vol_is_computed:
            self.current_sigma = EMA_ALPHA * raw + (1.0 - EMA_ALPHA) * self.current_sigma
        else:
            self.current_sigma = raw
        self.vol_is_computed = True

    @property
    def sigma(self) -> float:
        return self.current_sigma

    @property
    def ready(self) -> bool:
        return len(self.prices) >= 20 and self.vol_is_computed
