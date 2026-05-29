# Instrument Recommendation For A 10,000 CNY Account

## Direct Answer

For this account size, the recommended starting category is:

```text
liquid, low-price A-share ETF/fund or similar exchange-traded fund with a 100-unit board lot
```

Reason: the minimum tradable unit is small enough that a real stop can often fit
inside a 50-100 CNY risk budget.

In the included template, `qty=1` means one 100-unit board lot, not one single
ETF unit.

The second-best category is:

```text
US stock/ETF traded in small whole-share size, or fractional shares if the broker supports them
```

Reason: share count can be reduced to control risk. This is less "leveraged",
but it is more compatible with a small account than most futures contracts.

The category to avoid at the beginning is:

```text
normal futures contracts and most micro futures under a strict 0.5% risk budget
```

Reason: one contract's normal stop distance can exceed the account's allowed
loss. If the system rejects a futures ticket, the correct action is no trade.

## Why The System Still Matters

The point of the system is not to force a trade. The point is to say:

```text
This account can trade this candidate.
This account cannot trade that candidate.
No candidate fits today, so no trade.
```

A small account survives by rejecting mismatched opportunities. The system is
useful precisely because it can say no.

## How To Let The System Recommend Candidates

Run:

```powershell
python -m mlt.cli screen --universe universe.recommended_start.json --config config.live_guarded_10000_cny.json --contracts contracts.example.json --state account_state.example.json --out runs\recommended_screen
```

Read:

```text
runs\recommended_screen\screen_results.md
runs\recommended_screen\screen_results.json
```

Only candidates marked `READY` may proceed to manual ticket review.

## Current Template Universe

- `A_SHARE_LOW_PRICE_ETF_TEMPLATE`: intended starting category.
- `US_STOCK_OR_ETF_1_SHARE_TEMPLATE`: secondary category.
- `SAMPLE_FUT`: deliberately shows rejection for too-large futures risk.
- `CME_MICRO_INDEX_TEMPLATE`: paper-test only until exact broker specs and FX conversion are added.

These are templates, not live ticker recommendations. Replace each template with
real symbols, real historical bars, and verified broker contract specs before
placing money.
