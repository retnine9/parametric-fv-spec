# Parametric Fair Value: A Strategy Case Study

This repo is a write-up of a directional strategy for crypto Up/Down prediction markets. It covers the math and the decision rules. It is not a bot, not an SDK, and not something you can deploy by cloning the repo alone.

Think of it as a case study you can implement in your own stack if you already have (or plan to build) market discovery, feeds, and execution.

## What the strategy does

At each evaluation tick you hand it a market snapshot: spot, window open, time left, the order book, and your parameter set. It returns:

1. A probability that the window resolves UP (from realized vol, moneyness, and momentum)
2. Economics for each candidate trade (fees, depth sweep, reward per dollar locked)
3. A decision: enter UP, enter DOWN, or skip, plus a reason code

Pricing vol uses a simple realized-vol estimator. No GARCH. No machine learning.

## Before you start

The formulas alone will not run in production. You need plumbing this repo does not include:

- **A way to auto-find live Up/Down crypto markets** (rolling BTC/ETH/SOL 5m, 15m, 60m, 4h windows on Polymarket or similar: market IDs, token IDs, window open, resolution clock)
- A spot feed for the underlying
- L2 ask depth for UP and DOWN outcome tokens
- Something that actually sends orders to the CLOB

If you cannot discover live windows on your own, the worked examples and snippets are still useful for learning the model. You just cannot trade from this repo by itself.

Start with [docs/prerequisites.md](docs/prerequisites.md) and [docs/strategy-boundary.md](docs/strategy-boundary.md).

## Documentation map

| Doc | Topic |
|-----|--------|
| [prerequisites.md](docs/prerequisites.md) | What you need outside this repo |
| [market-context.md](docs/market-context.md) | What an Up/Down window is |
| [glossary.md](docs/glossary.md) | Symbols and units |
| [inputs.md](docs/inputs.md) | Snapshot fields and `evaluate()` contract |
| [vol-estimator.md](docs/vol-estimator.md) | Realized vol (non-GARCH) |
| [gbm-engine.md](docs/gbm-engine.md) | GBM digital P(UP) |
| [ou-engine.md](docs/ou-engine.md) | OU mean-reversion digital P(UP) |
| [momentum-and-blend.md](docs/momentum-and-blend.md) | Momentum and blend |
| [calibration.md](docs/calibration.md) | Isotonic and affine calibration |
| [fees.md](docs/fees.md) | Taker fee formula |
| [pes-economics.md](docs/pes-economics.md) | Depth sweep and reward scoring |
| [pes-gates.md](docs/pes-gates.md) | Gates and reason codes |
| [pes-selection.md](docs/pes-selection.md) | Picking the winning candidate |
| [parameters.md](docs/parameters.md) | Parameter dictionary |
| [strategy-boundary.md](docs/strategy-boundary.md) | In scope vs out of scope |

## Examples

- [worked-tick-gbm.md](examples/worked-tick-gbm.md): hand trace, GBM path
- [worked-tick-ou.md](examples/worked-tick-ou.md): same setup, OU enabled
- [worked-pes-entry.md](examples/worked-pes-entry.md): fair_p plus book to PES winner

Fixtures live in [examples/fixtures/](examples/fixtures/).

## Reference snippets

Small Python files in [reference/snippets/](reference/snippets/) mirror the docs. They are illustrative, not a library. If a snippet and a doc disagree, trust the doc.

Symbol definitions live in [glossary.md](docs/glossary.md).

## License

MIT. See [LICENSE](LICENSE).
