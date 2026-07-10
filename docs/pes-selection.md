# PES selection

## Steps

1. Build candidates: `{ENTER_UP, ENTER_DOWN} × size_buckets` (plus position actions if not flat)
2. For each: economics, score, gates
3. Drop blocked candidates
4. Pick highest `primary_score` (`duration_adjusted_reward`) among survivors
5. If none left: `SKIP` with `SKIP_NO_VIABLE_CANDIDATE`

## Ties

Compare with `score_tie_epsilon` (e.g. $10^{-12}$).

## Position states

| State | Behavior |
|-------|----------|
| Flat | Entries only |
| Long UP / DOWN | May pair-complete, hold, or exit |
| Cooldown | No new entries until elapsed |

## Pair complete

If long UP and you buy DOWN to lock \$1:

$$
\pi_{\mathrm{pair}} = 1 - c_{\mathrm{up}} - p_{\mathrm{down}} - f_{\mathrm{down}}
$$

per share, where $c_{\mathrm{up}}$ = held UP cost, $p_{\mathrm{down}}$ = avg exec on DOWN, $f_{\mathrm{down}}$ = fee per share on DOWN.

Take it when gates pass and the score beats alternatives.

## Legacy edge path (reference only)

Older parametric logic compared dampened edges to a dynamic threshold:

$$
{e_{\mathrm{up}}}^{\mathrm{raw}} = p - a_{\mathrm{up}} - f_{\mathrm{up}}
$$

where $a_{\mathrm{up}}$ = `ask_up`.

$$
\lambda = \frac{1}{1 + m \cdot |\Delta S / S_{0}|}
$$

$$
e_{\mathrm{up}} = {e_{\mathrm{up}}}^{\mathrm{raw}} \cdot \lambda
$$

$$
\tau_{\mathrm{thr}} = \tau_{0} \cdot (0.5 + t_{\mathrm{frac}}) \cdot m_{\sigma}
$$

Live selection uses PES, not this path. Kept here for backtest parity notes.

## Output

Winner executes at `size_usd` with `reason_code = SELECTED`, or skip with a specific gate reason.
