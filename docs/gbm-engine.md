# GBM engine: digital P(UP)

Default mean-reversion core when OU is off.

## Model

Log-moneyness:

$$
x = \ln\!\left(\frac{S}{S_{0}}\right)
$$

Time remaining in years (`N_yr` = `SECONDS_PER_YEAR`):

$$
t = \frac{T_{\mathrm{ms}}}{1000 \cdot N_{\mathrm{yr}}}
$$

where $T_{\mathrm{ms}}$ = `time_remaining_ms`.

Normalized distance:

$$
d = \frac{x}{\sigma\sqrt{t}}
$$

Mean-reversion probability:

$$
m_{r} = \Phi(d)
$$

If `student_t_dof` is in (0, 30), use the Student-t CDF instead of the normal CDF.

## Edge cases

When $\sigma\sqrt{t}$ is effectively zero:

| Sign of x | m_r |
|-----------|-----|
| positive | 0.99 |
| negative | 0.01 |
| zero | 0.50 |

Threshold: $\sigma\sqrt{t} < 10^{-12}$.

## Intuition

Spot above open gives x > 0 and m_r > 0.5. Less time left tightens the distribution toward 0 or 1. Higher sigma pulls m_r toward 0.5.

This is a digital "finish above open" probability, not full Black-Scholes with drift and discounting.

## When to use GBM

When `ou_enabled == false` or `ou_theta <= 0`.

## Snippet

[reference/snippets/gbm_fair_p.py](../reference/snippets/gbm_fair_p.py)
