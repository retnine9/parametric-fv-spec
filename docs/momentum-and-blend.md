# Momentum and blend

Combines mean-reversion $m_{r}$ with momentum $m_{p}$.

## Momentum probability

Over `momentum_lookback_secs`:

$$
\mathrm{slope} = \frac{S_{\mathrm{now}} - S_{\mathrm{old}}}{S_{\mathrm{old}}}
$$

$$
t_{\mathrm{lb}} = \frac{L}{N_{\mathrm{yr}}}
$$

where $L$ = `momentum_lookback_secs`.

$$
m_{p} = \Phi\!\left(\frac{\mathrm{slope}}{\sigma\sqrt{t_{\mathrm{lb}}}}\right)
$$

Invalid denominator: set $m_{p} = 0.5$.

## Trend boost

**Layer 1** (trend intensity from normalized moneyness):

- GBM: $|d|$ where $d = x / (\sigma\sqrt{t})$
- OU: $|e_{x} / \sqrt{v_{x}}|$

Smooth ramp from `trend_ramp_start` to `trend_ramp_full`:

$$
L_{1} = \mathrm{clip}\!\left(\frac{|z| - a_{1}}{b_{1} - a_{1}},\, 0,\, 1\right)
$$

where $a_{1}$ = `trend_ramp_start`, $b_{1}$ = `trend_ramp_full`.

**Layer 2** (persistence from rolling up-rate vs base):

$$
L_{2} = \mathrm{clip}\!\left(\frac{|\bar{u} - u_{0}| - a_{2}}{b_{2} - a_{2}},\, 0,\, 1\right)
$$

where $\bar{u}$ = `rolling_up_rate`, $u_{0}$ = `persistence_base_rate`, $a_{2}$ = `persistence_ramp_start`, $b_{2}$ = `persistence_ramp_full`.

$$
F = \max(L_{1}, L_{2})
$$

$$
{w_{\max}}^{\mathrm{eff}} = w_{\max} + (1 - w_{\max}) \cdot F \cdot b_{\mathrm{trend}}
$$

where $w_{\max}$ = `momentum_blend_max`, $b_{\mathrm{trend}}$ = `trend_boost_max`.

## Blend weight

$$
w = \mathrm{clip}\!\left(\frac{\sigma - \sigma_{\mathrm{low}}}{\sigma_{\mathrm{high}} - \sigma_{\mathrm{low}}},\, 0,\, 1\right) \cdot {w_{\max}}^{\mathrm{eff}}
$$

where $\sigma_{\mathrm{low}}$ = `momentum_blend_floor`, $\sigma_{\mathrm{high}}$ = `momentum_blend_ceiling`.

$$
p_{\mathrm{blend}} = (1 - w)\, m_{r} + w\, m_{p}
$$

If `momentum_blend_ceiling <= momentum_blend_floor`, set $w = 0$.

## Intuition

Low vol: trust moneyness ($m_{r}$). High vol plus strong trend or persistence: trust momentum ($m_{p}$).

## Snippet

[reference/snippets/blend_and_calibrate.py](../reference/snippets/blend_and_calibrate.py)
