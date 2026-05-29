# Project Status

## Complete

- Standalone folder independent from `FinMediaCrew`.
- Standard-library Python implementation.
- CSV loader with validation.
- Donchian breakout plus ATR stop strategy.
- Risk sizing by stop distance, multiplier, commission, slippage, and margin.
- Daily loss kill switch.
- Total drawdown kill switch.
- Manual order ticket JSON and Markdown output.
- Candidate universe screening command.
- Instrument recommendation file for a 10,000 CNY account.
- Backtest command.
- Signal command.
- Unit tests for risk, strategy, and backtest.
- Review entrypoint and acceptance checklist.
- IBKR paper-trading adapter requirements documented.
- 273 USD IBKR small-account guarded config documented.

## Intentionally Not Complete

- Live broker API execution.
- IBKR paper account execution.
- Broker-specific contract discovery.
- Real-time market data ingestion.
- Automatic rollover for futures continuous contracts.
- Portfolio-level multi-symbol capital allocator.
- Tax, borrow fee, funding fee, and exchange-specific rule modeling.

These are not hidden gaps. They are explicitly out of scope for this MVP because
auto-execution with real money requires broker-specific integration and separate
reconciliation tests.

## Current Verification Status

Verified on 2026-05-28:

```text
python -m unittest discover -s tests
Result: OK, 7 tests
```

The guarded sample ticket correctly rejects the sample trade because:

```text
risk budget = 50 CNY
risk per contract = 112 CNY
result = REJECTED / risk_budget_too_small
```

The paper-demo config can be used to verify READY ticket generation.
The recommended universe screen can be used to verify that low-unit instruments
are compatible with 10,000 CNY while larger futures-like risk is rejected.
