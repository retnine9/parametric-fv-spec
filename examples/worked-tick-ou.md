# Worked example: OU path

Same snapshot as [worked-tick-gbm.md](worked-tick-gbm.md), but `ou_enabled=true`, `ou_theta=0.02`, `ou_mu=0`.

Constants: $N_{\mathrm{yr}} = 31{,}557{,}600$, $\tau = 120$ s, $\theta = 0.02$, $x = 0.00514$.

## OU core

$$
e_{x} = x \cdot e^{-\theta \tau} = 0.00514 \times e^{-2.4} \approx 0.000466
$$

(since $\mu = 0$)

$$
\sigma_{\mathrm{sec}} = \frac{0.65}{\sqrt{N_{\mathrm{yr}}}} \approx 1.16 \times 10^{-4}
$$

$$
v_{x} = \frac{{\sigma_{\mathrm{sec}}}^{2}}{2\theta}\left(1 - e^{-2\theta\tau}\right) \approx 3.34 \times 10^{-8}
$$

$$
z = \frac{e_{x}}{\sqrt{v_{x}}} \approx 2.55
$$

$$
m_{r} = \Phi(2.55) \approx 0.994
$$

OU pulls expected log-moneyness toward zero, so $m_{r}$ is still high here but less extreme than GBM's $d \approx 4.05$ when the move is large relative to time left.

## Blend and calibration

Run the same momentum and blend steps as the GBM example with this $m_{r}$. Differences show up when momentum weight is material.

## When OU matters more

Push $|x|$ up and $\tau$ down: GBM stays glued near 0 or 1; OU keeps $e_{x}$ closer to $\mu$, so $m_{r}$ stays nearer 0.5.
