# Market context: Up/Down windows

Short background if you have never traded these markets.

## The instrument

A crypto Up/Down window is a short binary market:

- Underlying: spot on an asset (e.g. BTC)
- Window: fixed length (5m, 15m, 1h, 4h, etc.)
- Open: spot $S_{0}$ at window start (the strike for this window)
- End: spot $S_{T}$ at window end
- Resolution:
  - UP pays **\$1** if $S_{T} \ge S_{0}$
  - DOWN pays **\$1** if $S_{T} < S_{0}$
  - The loser pays **\$0**

Before resolution, UP and DOWN tokens trade on a CLOB roughly between \$0.01 and \$0.99.

## What the strategy is trying to do

Before the window ends, it asks: given spot, open, vol, time left, and the books, is buying UP or DOWN at a given size positive expected value after fees?

It outputs a discrete action (enter UP, enter DOWN, skip), not a hedge in the underlying.

## Not in this write-up

- Will / barrier / bracket markets (different payoff geometry)
- Spread capture (buying both sides when combined ask is under \$1)
- Market making or end-of-window-only rules
- Finding which windows exist right now ([prerequisites.md](prerequisites.md) covers that)

## Parameters per market

Each `(asset, window_duration)` pair can use its own tuning (vol floor, blend weights, PES thresholds). You pass the right set for the market you are evaluating.
