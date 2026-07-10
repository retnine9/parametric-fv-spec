# Volatility estimator (non-GARCH)

Pricing vol (sigma) is realized vol from spaced spot returns. GARCH is not used for pricing in this case study.

## Steps

1. Sample prices at least 5 seconds apart (ignore closer ticks).
2. For each consecutive pair $(t_{i-1}, S_{i-1})$, $(t_i, S_i)$:
   - $\Delta t$ in seconds (must be at least 5 and less than 120)
   - Return rate: $r_{i} = \ln(S_{i} / S_{i-1}) / \sqrt{\Delta t}$
3. Keep samples inside `vol_window_secs` (e.g. 300s).
4. Sample variance over returns (n >= 5):

   $$
   \sigma_{\mathrm{sec}} = \sqrt{\mathrm{Var}(r)}
   $$

5. Annualize:

   $$
   \sigma_{\mathrm{raw}} = \sigma_{\mathrm{sec}} \cdot \sqrt{N_{\mathrm{yr}}}
   $$

6. Clamp:

   $$
   \sigma = \mathrm{clamp}(\sigma_{\mathrm{raw}},\,\sigma_{\mathrm{floor}},\,\sigma_{\mathrm{ceiling}})
   $$

7. EMA smooth after first valid value:

   $$
   \sigma \leftarrow 0.3\,\sigma_{\mathrm{raw}} + 0.7\,\sigma_{\mathrm{prev}}
   $$

## Readiness

| Condition | Behavior |
|-----------|----------|
| fewer than 5 returns | sigma = floor, not computed |
| at least 5 returns | computed = true |
| at least 20 price samples | ready = true (typical pre-trade gate) |

## Parameters

| Parameter | Typical role |
|-----------|--------------|
| `vol_window_secs` | Lookback (e.g. 300) |
| `vol_floor` | Min sigma (e.g. 0.25) |
| `vol_ceiling` | Max sigma (e.g. 0.80) |

## Common mistakes

- Tick-by-tick returns without 5s spacing inflate sigma.
- Feeding per-second sigma into GBM. GBM wants annualized sigma with t in years.
- Swapping in GARCH or implied vol. Out of scope here.

## Snippet

[reference/snippets/vol_estimator.py](../reference/snippets/vol_estimator.py)
