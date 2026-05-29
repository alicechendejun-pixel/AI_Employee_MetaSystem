# Runbook

All commands run from this folder.

## 1. Verify The Code

```powershell
python -m unittest discover -s tests
python -m py_compile mlt\models.py mlt\data.py mlt\indicators.py mlt\strategy.py mlt\risk.py mlt\tickets.py mlt\backtest.py mlt\cli.py
```

## 2. Run A Guarded Backtest

```powershell
python -m mlt.cli backtest --bars data\sample_ohlcv.csv --symbol SAMPLE_FUT --config config.live_guarded_10000_cny.json --contracts contracts.example.json --out runs\guarded_backtest
```

Read:

```text
runs\guarded_backtest\backtest_result.json
```

## 3. Generate A Real-Money-Guarded Ticket

```powershell
python -m mlt.cli signal --bars data\sample_ohlcv.csv --symbol SAMPLE_FUT --config config.live_guarded_10000_cny.json --contracts contracts.example.json --state account_state.example.json --out runs\guarded_signal
```

Read:

```text
runs\guarded_signal\latest_ticket.md
runs\guarded_signal\latest_ticket.json
```

If the ticket says `REJECTED`, do not trade. The rejection reason is the system's
decision.

## 4. Demonstrate A READY Ticket In Paper Mode

```powershell
python -m mlt.cli signal --bars data\sample_ohlcv.csv --symbol SAMPLE_FUT --config config.paper_demo_acceptance.json --contracts contracts.example.json --state account_state.example.json --out runs\paper_demo_signal
```

This is for software acceptance only. It proves the system can produce a READY
ticket when the risk budget is intentionally relaxed.

## 5. Screen The Recommended Starting Universe

```powershell
python -m mlt.cli screen --universe universe.recommended_start.json --config config.live_guarded_10000_cny.json --contracts contracts.example.json --state account_state.example.json --out runs\recommended_screen
```

Read:

```text
runs\recommended_screen\screen_results.md
```

For a 10,000 CNY account, the intended starting category is low-price ETF/fund
style instruments with small board-lot risk. Futures-like candidates may be
rejected, and that is valid.

## 6. Replace Sample Contract Specs Before Any Real Trade

Edit a copied contract file, for example:

```text
contracts.my_broker.json
```

Required fields:

- `symbol`
- `multiplier`
- `tick_size`
- `margin_rate`
- `min_qty`
- `currency`
- `description`

The values must match the broker order screen. Do not use `SAMPLE_FUT` for real
money.

## 7. Replace Sample Market Data

Create a CSV with:

```text
date,open,high,low,close,volume
```

Then run:

```powershell
python -m mlt.cli backtest --bars path\to\your_data.csv --symbol YOUR_SYMBOL --config config.live_guarded_10000_cny.json --contracts contracts.my_broker.json --out runs\your_backtest
python -m mlt.cli signal --bars path\to\your_data.csv --symbol YOUR_SYMBOL --config config.live_guarded_10000_cny.json --contracts contracts.my_broker.json --state account_state.example.json --out runs\your_signal
```

## 8. Manual Execution Checklist

Only consider manual execution if:

- ticket status is `READY`
- broker contract symbol matches the ticket
- multiplier matches broker screen
- tick size matches broker screen
- commission estimate is not understated
- margin requirement is not understated
- protective stop is entered at the same time as the entry order
- daily loss kill switch is not active
- total drawdown kill switch is not active
- market is liquid and spread is normal
