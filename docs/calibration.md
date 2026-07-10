# Calibration

Maps $p_{\mathrm{blend}}$ to `fair_p_up`.

## Isotonic (when tables exist)

If `isotonic_x` and `isotonic_y` are non-empty and same length:

$$
p = \mathrm{interp}(p_{\mathrm{blend}},\; x_{\mathrm{iso}},\; y_{\mathrm{iso}})
$$

Linear interpolation on the isotonic table; clamp to $[0.01,\, 0.99]$.

Tables are usually fit offline on historical blended probs vs realized UP. Fitting procedure is not part of this case study.

## Affine fallback

When there is no isotonic table:

$$
\delta = c_{0} + c_{\sigma} \cdot \sigma
$$

$$
p = \mathrm{clip}\bigl(0.5 + (p_{\mathrm{blend}} - 0.5)\, s + \delta,\; 0.01,\; 0.99\bigr)
$$

where $c_{0}$ = `cal_drift`, $c_{\sigma}$ = `cal_drift_sigma`, $s$ = `cal_scale`.

## Downstream use

`fair_p_up` is the calibrated UP win probability for PES.

## Snippet

[reference/snippets/blend_and_calibrate.py](../reference/snippets/blend_and_calibrate.py)
