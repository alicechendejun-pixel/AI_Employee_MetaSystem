# Broker Adapters

No live broker adapter is implemented in this MVP.
No IBKR paper adapter is implemented in this MVP.

This is intentional. Automatic live execution requires broker-specific work:

- authentication
- account permission checks
- contract lookup
- order placement
- protective stop/bracket order placement
- fill reconciliation
- partial-fill handling
- cancellation and replace handling
- disconnect recovery
- broker-side margin and risk checks

The current system stops at manual ticket generation. A future adapter must
implement these interfaces without bypassing `mlt.risk.size_order` or the
kill-switch checks.

For IBKR specifically, start from `../IBKR_PAPER_TRADING_PLAN.md`.

Do not claim this folder supports live execution until an adapter has its own
tests and paper-trading logs.
