# OU engine: mean-reverting digital P(UP)

Optional replacement for GBM when `ou_enabled` and `ou_theta > 0`.

## Dynamics

Log-moneyness mean-reverts to $\mu$ at speed $\theta$ (per second). Time remaining $\tau$ is in **seconds**:

$$
e_{x} = \mu_{\mathrm{eff}} + (x - \mu_{\mathrm{eff}})\, e^{-\theta \tau}
$$

$$
\sigma_{\mathrm{sec}} = \frac{\sigma}{\sqrt{N_{\mathrm{yr}}}}
$$

$$
v_{x} = \frac{{\sigma_{\mathrm{sec}}}^{2}}{2\theta}\left(1 - e^{-2\theta \tau}\right)
$$

$$
m_{r} = \Phi\!\left(\frac{e_{x}}{\sqrt{v_{x}}}\right)
$$

Student-t applies the same way as GBM if `student_t_dof` is in $(0, 30)$.

## Adaptive $\mu$ (optional)

When `adaptive_mu_enabled` and `rolling_up_rate >= 0`:

$$
\mu_{\mathrm{eff}} = \mu + \mathrm{clip}\bigl((\bar{u} - u_{0})\, k,\,-\mu_{\max},\,+\mu_{\max}\bigr)
$$

where $\bar{u}$ = `rolling_up_rate`, $u_{0}$ = `persistence_base_rate`, $k$ = `adaptive_mu_sensitivity`, $\mu_{\max}$ = `adaptive_mu_max`.

## Edge cases

If $v_{x} < 10^{-24}$, clamp $m_{r}$ to 0.99, 0.01, or 0.50 by the sign of $e_{x}$.

## Why bother with OU

GBM lets log-moneyness drift like a random walk. Late in the window, after a big move, GBM can stay pinned near 0 or 1. OU pulls expected log-moneyness back toward $\mu$, so the model mean-reverts inside the probability itself.

High-vol regimes can swap `ou_theta` and `ou_mu` via HV parameters ([parameters.md](parameters.md)).

## Snippet

[reference/snippets/ou_fair_p.py](../reference/snippets/ou_fair_p.py)
