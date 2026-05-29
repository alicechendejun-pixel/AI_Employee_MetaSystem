# Acceptance Checklist

Use this checklist to decide whether the folder is complete enough for handoff.

## Folder Completeness

- [ ] `README.md` explains purpose, quick start, and safety model.
- [ ] `AI_REVIEW_ENTRYPOINT.md` gives third-party reviewer commands.
- [ ] `SYSTEM_SPEC.md` defines system boundaries and non-goals.
- [ ] `RUNBOOK.md` gives operational steps for backtest, signal, and manual ticket use.
- [ ] `PROJECT_STATUS.md` states what is complete and what is intentionally not complete.
- [ ] `RISK_DISCLOSURE.md` states real-money and leverage risks.
- [ ] `INSTRUMENT_RECOMMENDATION.md` states recommended starting categories for 10,000 CNY.
- [ ] `IBKR_PAPER_TRADING_PLAN.md` states broker API status and future paper adapter requirements.
- [ ] `IBKR_273_USD_LIVE_READINESS.md` states whether a 273 USD IBKR account can be used and with what scope.
- [ ] `universe.recommended_start.json` exists for candidate screening.
- [ ] `config.live_guarded_10000_cny.json` exists as the default guarded 10,000 CNY config.
- [ ] `contracts.example.json` exists and marks sample specs as replace-before-trading.
- [ ] `account_state.example.json` exists for kill-switch inputs.
- [ ] `data/sample_ohlcv.csv` exists for deterministic verification.
- [ ] `tests/` exists and covers strategy, risk, and backtest behavior.

## Functional Verification

- [ ] `python -m unittest discover -s tests` passes.
- [ ] `python -m py_compile ...` passes for all `mlt/*.py` files.
- [ ] Backtest command writes `backtest_result.json`.
- [ ] Signal command writes `latest_ticket.json` and `latest_ticket.md`.
- [ ] Screen command writes `screen_results.json` and `screen_results.md`.
- [ ] Guarded 10,000 CNY config rejects a sample trade when per-contract risk is greater than risk budget.
- [ ] Guarded universe screen can produce at least one READY low-unit template candidate.
- [ ] IBKR 273 USD universe screen runs and rejects futures-like candidates.
- [ ] Paper/demo config can produce a READY sample ticket when risk budget is intentionally relaxed.

## Risk Controls

- [ ] Every non-FLAT signal has an explicit stop.
- [ ] Position size is capped by stop-loss risk.
- [ ] Position size is capped by margin room.
- [ ] Commission and slippage are included in per-contract risk.
- [ ] Daily loss kill switch can reject a signal.
- [ ] Total drawdown kill switch can reject a signal.
- [ ] Short trades can be disabled by config.
- [ ] Output ticket includes human review checklist.

## Explicit Non-Goals For This MVP

- [ ] No live broker API execution is claimed complete.
- [ ] No IBKR paper API execution is claimed complete.
- [ ] No guaranteed return or profit target is claimed.
- [ ] No real A-share, US stock, or futures contract is pre-approved for trading.
- [ ] No order should be placed unless actual broker contract specs match config.
