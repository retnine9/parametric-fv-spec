# Worked example: GBM path

Synthetic BTC 5m window, 120 seconds left. Hand trace of the probability stack (PES comes later).

## Setup

| Field | Value |
|-------|-------|
| Spot S | 97,500 |
| Open S_0 | 97,000 |
| sigma (annualized) | 0.65 |
| Time remaining | 120,000 ms |
| slope | +0.0015 |

Illustrative params: `momentum_blend_floor=0.30`, ceiling `0.80`, `momentum_blend_max=0.50`, affine cal with `cal_scale=1.0`, `cal_drift=0`.

Constants: N_yr = 31,557,600.

## Step 1: log-moneyness

$$
x = \ln\!\left(\frac{97500}{97000}\right) \approx 0.00514
$$

## Step 2: GBM m_r

$$
t = \frac{120}{N_{\mathrm{yr}}} \approx 3.80 \times 10^{-6}\ \mathrm{years}
$$

$$
\sqrt{t} \approx 0.00195
$$

$$
d = \frac{0.00514}{0.65 \times 0.00195} \approx 4.05
$$

$$
m_{r} = \Phi(4.05) \approx 0.99997 \;\Rightarrow\; \mathrm{clamp\ to\ } 0.99
$$

Spot is slightly above open with little time left, so GBM is very confident UP.

## Step 3: momentum m_p

Lookback 60s:

$$
t_{\mathrm{lb}} = \frac{60}{N_{\mathrm{yr}}}
$$

$$
m_{p} = \Phi\!\left(\frac{0.0015}{0.65\sqrt{t_{\mathrm{lb}}}}\right) \approx \Phi(0.84) \approx 0.80
$$

## Step 4: blend

$$
w = \frac{0.65 - 0.30}{0.80 - 0.30} \times 0.50 = 0.35
$$

$$
p_{\mathrm{blend}} = 0.65 \times 0.99 + 0.35 \times 0.80 \approx 0.9235
$$

## Step 5: calibration

Affine defaults give `fair_p_up` of about 0.92 (clamp below 0.99 if needed).

## Common mistakes

- Using sigma = 0.65 as per-second in GBM (it is annualized).
- Using 120s directly as t in GBM (convert to years via N_yr).
- Forgetting clamp when d is very large.

Next: [worked-pes-entry.md](worked-pes-entry.md) uses a book with this fair_p.
