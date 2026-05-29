# IBKR Paper Trading Plan

## Current State

This system includes:

- a read-only connection probe
- a paper-only order-write probe

The paper order-write probe is still not a strategy executor. It only proves
that the API can write to a DU paper account under paper-port guards. The current
paper/virtual workflows are:

- backtest on historical CSV
- screen a candidate universe
- generate manual order tickets
- inspect risk before any broker action
- optionally connect read-only to TWS Paper and read account/position/open-order state
- optionally stage a non-transmitted paper order to prove API order-write access

## Can This Run Directly In An IBKR Paper Account?

Only for probing.

It can stage an untransmitted paper order. Strategy-to-order execution is not
implemented yet.

## Current Read-Only Probe

Run after TWS Paper is open and API socket is enabled:

```powershell
python broker_adapters\ibkr_readonly_probe.py --config config.ibkr_paper.template.json --out runs\ibkr_readonly_probe
```

Expected output includes:

- `connected: true`
- `managed_accounts`, usually a `DU...` paper account
- account summary fields if available
- positions
- open order count

If TWS shows a connection prompt, accept only if the client is localhost and the
port is the paper port.

## Current Paper Order-Write Probe

First disable `Read-Only API` in TWS Paper if you want to test write access.
Keep the account in Paper Trading.

Safe staged order probe:

```powershell
python broker_adapters\ibkr_paper_order_probe.py --config config.ibkr_paper.template.json --out runs\ibkr_paper_order_probe
```

Default behavior:

- paper ports only
- DU paper account only
- symbol `AAPL`
- quantity `1`
- limit price `1.00`
- `transmit=false`, so it is staged/untransmitted

To actually transmit and immediately cancel a paper order, an explicit flag is
required:

```powershell
python broker_adapters\ibkr_paper_order_probe.py --config config.ibkr_paper.template.json --out runs\ibkr_paper_order_probe_transmit --transmit --confirm-paper-order
```

Do not run the transmit command unless TWS is confirmed to be in Paper Trading.

## Recommended IBKR API Path

For this Windows workstation, the preferred first adapter is:

```text
TWS API or IB Gateway socket API
```

Reason: it is the standard IBKR path for local trading applications and can be
restricted to paper ports.

Default paper ports from IBKR documentation:

- TWS Paper: `7497`
- IB Gateway Paper: `4002`

Default live ports:

- TWS Live: `7496`
- IB Gateway Live: `4001`

The adapter must refuse live ports by default.

## Required IBKR Paper Order Adapter Features

Before any IBKR paper order is allowed, the adapter must implement:

- connection health check
- account summary read
- contract lookup
- market data or delayed data read
- position read
- open order read
- order preview or margin check where available
- bracket order placement in paper only
- protective stop attached to entry
- fill and partial-fill reconciliation
- cancel/replace handling
- disconnect recovery
- paper/live port guard

## Suggested Future Commands

These commands do not exist yet. They define the intended interface:

```powershell
python -m mlt.cli ibkr-status --config config.ibkr_paper.template.json
python -m mlt.cli ibkr-paper-place --ticket runs\your_signal\latest_ticket.json --config config.ibkr_paper.template.json --confirm-paper
python -m mlt.cli ibkr-paper-sync --config config.ibkr_paper.template.json --out runs\ibkr_sync
```

## Why A-Shares Are Not 24-Hour And Still Usable

This system does not require 24-hour trading.

For A-shares or ETFs, the workflow is:

1. update data after the market close
2. run screen/backtest/signal
3. prepare next-session ticket
4. place manually during market hours if the ticket is still valid

This is slower than futures or crypto, but slower is not a defect for a small
account. The main constraint is position sizing, not 24-hour access.

## If Using US Stocks Through IBKR

For your IBKR US stock account, the natural next step is:

```text
IBKR paper account first, US stocks/ETFs only, one-share or fractional-size risk.
```

The current system can generate the signal and ticket locally. It cannot yet
send that ticket into IBKR Paper automatically.
