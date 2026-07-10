# Glossary

## Symbols

| Symbol | Name | Units | Notes |
|--------|------|-------|-------|
| `S` | Spot | USD (or quote) | Current underlying |
| `S_0` | Window open | Same as spot | Strike at window start |
| `sigma` | Volatility | Annualized decimal | From VolEstimator; not GARCH here |
| `tau` | Time remaining | Seconds (OU); years (GBM) | Do not mix units |
| `x` | Log-moneyness | dimensionless | ln(S / S_0) |
| `m_r` | Mean-reversion prob | 0 to 1 | GBM or OU P(UP) before blend |
| `m_p` | Momentum prob | 0 to 1 | From slope over lookback |
| `p_blend` | Blended prob | 0 to 1 | Before calibration |
| `fair_p_up` | Calibrated UP prob | 0 to 1 | Output of calibration |
| slope | Momentum input | dimensionless | (S_now - S_old) / S_old |

In other docs, the same symbols appear in display formulas using standard math notation.

## Constants

| Constant | Value | Code name |
|----------|-------|-----------|
| `N_yr` | 31,557,600 | `SECONDS_PER_YEAR` |

GBM time in years:

$$
t = \frac{T_{\mathrm{ms}}}{1000 \cdot N_{\mathrm{yr}}}
$$

where $T_{\mathrm{ms}}$ = `time_remaining_ms`, and $N_{\mathrm{yr}}$ is `SECONDS_PER_YEAR`.

## Decision outputs

| Field | Meaning |
|-------|---------|
| `action` | `ENTER_UP`, `ENTER_DOWN`, `SKIP`, `HOLD`, etc. |
| `size_usd` | Target notional for entries |
| `reason_code` | Why selected or skipped (e.g. `SKIP_PIN_RISK`) |
| `primary_score` | `duration_adjusted_reward` for entries |

## Deliberately excluded

- GARCH / `sigma_garch` for pricing vol ([vol-estimator.md](vol-estimator.md))
- ML `fair_p` from a classifier (different path)
- Market discovery ([prerequisites.md](prerequisites.md))
