# Polymarket taker fee

Size-aware fee for Up/Down windows with taker fees enabled.

## Formula

```text
p = clamp(price, 0.01, 0.99)
q = p * (1 - p)
raw = shares * p * 0.25 * q^2
fee_total = round(raw, 4 decimal places)
if fee_total > 0: fee_total = max(fee_total, 0.0001)
else: fee_total = 0
fee_per_share = fee_total / shares
```

## Rules

1. Round **after** `shares * rate`. Do not round per-share first and multiply.
2. Use average execution price from the depth sweep, not the top of book alone.
3. Windows without taker fees return 0 (venue-specific; crypto Up/Down usually has fees).

## Example

Price = 0.40, shares = 50:

```text
q = 0.40 * 0.60 = 0.24
raw = 50 * 0.40 * 0.25 * 0.24^2 = 0.288
fee_total = 0.2880
fee_per_share = 0.00576
```

## Snippet

[reference/snippets/polymarket_fee.py](../reference/snippets/polymarket_fee.py)
