# AI Review Entrypoint

This folder is a standalone trading-system MVP.

Reviewer instruction:

1. Read this file first.
2. Run the commands below from this folder.
3. Judge the system against `ACCEPTANCE_CHECKLIST.md`.
4. Do not evaluate sibling projects such as `FinMediaCrew`; this folder is independent.

## What This System Is

`10K_CNY_MicroLeverage_TradingSystem_小资金杠杆交易系统` is a local, auditable
small-capital leverage trading workflow:

- historical CSV data in
- strategy signal generated
- risk sizing applied
- margin and kill-switch checks applied
- manual order ticket produced
- backtest report produced

It is intentionally not connected to a live broker yet. Broker execution is a
separate adapter layer and must not be assumed complete.

## Required Verification Commands

```powershell
python -m unittest discover -s tests
python -m py_compile mlt\models.py mlt\data.py mlt\indicators.py mlt\strategy.py mlt\risk.py mlt\tickets.py mlt\backtest.py mlt\cli.py
python -m mlt.cli backtest --bars data\sample_ohlcv.csv --symbol SAMPLE_FUT --config config.live_guarded_10000_cny.json --contracts contracts.example.json --out runs\review_backtest
python -m mlt.cli signal --bars data\sample_ohlcv.csv --symbol SAMPLE_FUT --config config.live_guarded_10000_cny.json --contracts contracts.example.json --state account_state.example.json --out runs\review_signal
python -m mlt.cli screen --universe universe.recommended_start.json --config config.live_guarded_10000_cny.json --contracts contracts.example.json --state account_state.example.json --out runs\review_screen
python -m mlt.cli screen --universe universe.ibkr_273_usd_start.json --config config.live_guarded_273_usd_ibkr.json --contracts contracts.example.json --state account_state_273_usd.example.json --out runs\review_ibkr_273_screen
```

Expected:

- tests pass
- py_compile returns no error
- `runs/review_backtest/backtest_result.json` exists
- `runs/review_signal/latest_ticket.json` exists
- `runs/review_screen/screen_results.json` exists
- `runs/review_ibkr_273_screen/screen_results.json` exists
- with guarded live config, sample signal is rejected because per-contract stop risk exceeds the 50 CNY risk budget

That rejection is a correct risk-control result, not a failure.
The universe screen should show at least one READY template candidate and at least
one rejected futures-like candidate.

## Optional Software-Demo Command

This command uses a paper/demo config with a larger risk budget to prove the
same engine can accept a trade when risk and margin allow it. It is not the
recommended real-money config.

```powershell
python -m mlt.cli signal --bars data\sample_ohlcv.csv --symbol SAMPLE_FUT --config config.paper_demo_acceptance.json --contracts contracts.example.json --state account_state.example.json --out runs\review_signal_demo
```

Expected:

- `runs/review_signal_demo/latest_ticket.json` has `"status": "READY"`
