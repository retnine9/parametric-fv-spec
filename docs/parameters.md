# Parameters

One bundle per `(asset, window_duration)`. Schema: [schema/params.schema.json](../schema/params.schema.json). Example: [examples/fixtures/params_btc_5m.example.json](../examples/fixtures/params_btc_5m.example.json).

## Volatility

| Key | Description |
|-----|-------------|
| `vol_window_secs` | Return lookback |
| `vol_floor` | sigma floor (annualized) |
| `vol_ceiling` | sigma ceiling (annualized) |

## Probability engine

| Key | Description |
|-----|-------------|
| `ou_enabled` | OU instead of GBM |
| `ou_theta` | Mean reversion speed (1/sec) |
| `ou_mu` | Long-run log-moneyness mean |
| `student_t_dof` | In (0,30): Student-t CDF |
| `adaptive_mu_enabled` | Shift μ from rolling up-rate |
| `adaptive_mu_sensitivity` | μ correction scale |
| `adaptive_mu_max` | Max \|μ adjustment\| |

## Momentum and blend

| Key | Description |
|-----|-------------|
| `momentum_lookback_secs` | Slope lookback |
| `momentum_blend_floor` | sigma where blend weight w = 0 |
| `momentum_blend_ceiling` | sigma where w hits max |
| `momentum_blend_max` | Cap on momentum weight |
| `trend_boost_max` | Trend boost cap |
| `trend_ramp_start`, `trend_ramp_full` | Layer 1 ramp |
| `persistence_base_rate` | Base UP rate for layer 2 |
| `persistence_ramp_start`, `persistence_ramp_full` | Layer 2 ramp |

## Calibration

| Key | Description |
|-----|-------------|
| `cal_scale` | Affine scale on centered prob |
| `cal_drift` | Affine drift |
| `cal_drift_sigma` | Drift term scaled by sigma |
| `isotonic_x`, `isotonic_y` | Optional tables |

## PES

| Key | Description |
|-----|-------------|
| `pes_size_buckets_usd` | e.g. [10, 20] |
| `pes_score_threshold` | Min primary_score |
| `pes_min_expected_reward_dollars` | Min expected reward (USD) |
| `pes_min_expected_reward_per_share` | Min reward per share (USD) |
| `pes_min_lockup_floor` | Duration score denominator floor |
| `pes_max_spread` | Spread gate (AND both sides) |
| `pes_max_quote_age_ms` | Max book age |

## High-vol regime (optional)

When `sigma >= regime_boundary_high`, you may override `hv_ou_theta`, `hv_ou_mu`, `hv_min_conviction`, etc.

## Legacy edge (diagnostic)

| Key | Description |
|-----|-------------|
| `edge_threshold` | Legacy threshold scale |
| `mean_reversion_factor` | Edge dampening |
| `vol_dampening_reference`, `vol_dampening_power` | Dampening vs sigma |

Not used for primary PES selection.
