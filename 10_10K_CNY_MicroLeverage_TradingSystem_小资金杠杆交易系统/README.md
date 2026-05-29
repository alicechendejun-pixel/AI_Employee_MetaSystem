# 10K CNY Micro Leverage Trading System

Small-capital, risk-first trading research and ticketing system.

This is not a profit-guarantee engine and it does not auto-place live orders by
default. It is built for one job: make every trade explicit before real money is
used.

## Why This Exists

The sibling `FinMediaCrew` project is a financial media/content workflow. It is
not a trading system. It has no account ledger, broker adapter, order state,
fill handling, margin checks, or kill switch.

`micro_leverage_trader` is a separate system with those boundaries:

- load OHLCV data from CSV
- generate trend-following signals
- size positions from account risk, stop distance, contract multiplier, and margin
- backtest with conservative stop handling
- output human-readable order tickets for manual execution
- keep live execution off until a broker adapter is explicitly added and tested

## Default Strategy

The included strategy is a Donchian breakout with ATR stops:

- Long: latest close breaks the previous N-bar high and is above SMA trend filter.
- Short: latest close breaks the previous N-bar low and is below SMA trend filter.
- Stop: ATR multiple from the signal close.
- Target: fixed R multiple from entry to stop.

This is intentionally simple. The edge, if any, must come from market selection,
cost control, and risk discipline, not from hidden model complexity.

## Real-Money Guardrails

The default config is intentionally restrictive for a CNY 10,000 account:

- 0.5% risk per trade
- 35% maximum margin use
- 1.5% daily loss stop
- no live broker execution
- every generated trade must include a stop

For futures, margin is not a down payment. Losses can move faster than the
posted margin, and your broker can require more margin than the exchange.

## Quick Start

From this folder:

```powershell
python -m unittest discover -s tests
python -m mlt.cli backtest --bars data/sample_ohlcv.csv --symbol SAMPLE_FUT --config config.live_guarded_10000_cny.json --contracts contracts.example.json --out runs/sample
python -m mlt.cli signal --bars data/sample_ohlcv.csv --symbol SAMPLE_FUT --config config.live_guarded_10000_cny.json --contracts contracts.example.json --state account_state.example.json --out runs/latest
python -m mlt.cli screen --universe universe.recommended_start.json --config config.live_guarded_10000_cny.json --contracts contracts.example.json --state account_state.example.json --out runs/recommended_screen
```

The `signal` command writes a ticket JSON and Markdown file under `runs/latest`.
Use that ticket as a manual checklist in your broker app. Do not place the order
if the broker's actual multiplier, tick size, fee, margin, or tradability differs
from `contracts.example.json`.

Third-party AI reviewers should start with `AI_REVIEW_ENTRYPOINT.md`.
Instrument category guidance is in `INSTRUMENT_RECOMMENDATION.md`.
IBKR paper-trading status and adapter requirements are in `IBKR_PAPER_TRADING_PLAN.md`.
IBKR 273 USD live-readiness notes are in `IBKR_273_USD_LIVE_READINESS.md`.

## Data Format

CSV columns:

```text
date,open,high,low,close,volume
```

Dates can be daily bars or intraday timestamps. Keep them in chronological order.

## Making It Practical

Before using real money:

1. Replace `SAMPLE_FUT` in `contracts.example.json` with your broker's exact
   tradable contract specs.
2. Export at least several years of continuous historical bars for the chosen
   contract or a correctly adjusted main-continuous series.
3. Backtest with realistic commission and slippage.
4. Paper trade at least 30 signals.
5. Start with one minimum-size contract only if the generated stop risk is within
   the configured risk budget.

## Files

- `mlt/data.py`: CSV loading and validation.
- `mlt/strategy.py`: signal generation.
- `mlt/risk.py`: position sizing and margin gates.
- `mlt/backtest.py`: conservative backtest engine.
- `mlt/tickets.py`: manual order ticket output.
- `mlt/cli.py`: command line entrypoint.
- `account_state.example.json`: equity, daily PnL, and open margin for kill switches.
- `ACCEPTANCE_CHECKLIST.md`: exact handoff checklist.
- `IBKR_PAPER_TRADING_PLAN.md`: states that broker API integration is not implemented yet.
- `tests/`: regression tests for the risk, strategy, and backtest layers.
