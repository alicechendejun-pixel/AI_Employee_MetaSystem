# Handoff To Claude Code Opus 4.7

## Immediate Mission

Continue this project from here:

```text
G:\我的云端硬盘\09-AI员工系统\10K_CNY_MicroLeverage_TradingSystem_小资金杠杆交易系统
```

Implement **IBKR Paper Adapter v0.2**:

```text
Take an existing latest_ticket.json from this system and place a real paper-account bracket order in IBKR TWS Paper.
```

Do **not** connect to live trading. Do **not** use live ports.

## Current Verified State

TWS Paper is running on this Windows machine.

Verified by Codex:

- TWS Paper socket: `127.0.0.1:7497`
- Managed account: `DUE972820`
- Account type: DU paper account
- `ibapi` installed: `ibapi-9.81.1.post1`
- Read account summary: success
- Read positions: success
- Read open orders: success
- Paper order write path: success through IBKR `whatIf` order
- Last successful probe: AAPL 1 share limit order, `whatIf=true`, returned `PreSubmitted`
- No positions and no open orders remained after probe

Important fix already applied:

```python
order.eTradeOnly = False
order.firmQuoteOnly = False
```

The pip `ibapi` package defaults these deprecated flags to `True`; recent TWS rejects them.

## Existing IBKR Files

Read these first:

```text
IBKR_PAPER_TRADING_PLAN.md
IBKR_273_USD_LIVE_READINESS.md
config.ibkr_paper.template.json
broker_adapters\ibkr_readonly_probe.py
broker_adapters\ibkr_paper_order_probe.py
```

Run these before changing anything:

```powershell
python broker_adapters\ibkr_readonly_probe.py --config config.ibkr_paper.template.json --out runs\ibkr_readonly_probe --timeout 10
python broker_adapters\ibkr_paper_order_probe.py --config config.ibkr_paper.template.json --out runs\ibkr_paper_order_probe_whatif --timeout 10 --client-id 189
```

Expected:

- `connected: true`
- account starts with `DU`
- no live port
- no open order residue
- order write probe reaches IBKR order validation path

## Safety Rules

Hard rules:

- Only allow paper ports:
  - TWS Paper: `7497`
  - IB Gateway Paper: `4002`
- Refuse live ports:
  - TWS Live: `7496`
  - IB Gateway Live: `4001`
- Refuse any account that does not start with `DU`
- Refuse missing stop order
- Refuse `latest_ticket.json` if status is not `READY`
- Refuse order if ticket quantity is `0`
- Refuse order if side is not supported
- Default to paper only
- Require explicit CLI flag before transmitting any paper order
- After any transmitted test order, read open orders and positions

Do not add auto-live trading.

## User Account Context

User has an IBKR account with about `273 USD` real cash, but the current work must
continue in Paper Trading first.

The user wants to eventually trade small US stock/ETF positions, not futures or
options at this stage.

Use:

```text
config.live_guarded_273_usd_ibkr.json
account_state_273_usd.example.json
universe.ibkr_273_usd_start.json
```

## Next Implementation Target

Create a new file:

```text
broker_adapters\ibkr_paper_ticket_executor.py
```

Suggested CLI:

```powershell
python broker_adapters\ibkr_paper_ticket_executor.py --ticket runs\paper_demo_signal\latest_ticket.json --config config.ibkr_paper.template.json --what-if --client-id 201
```

Then:

```powershell
python broker_adapters\ibkr_paper_ticket_executor.py --ticket runs\paper_demo_signal\latest_ticket.json --config config.ibkr_paper.template.json --transmit --confirm-paper-order --client-id 202
```

## Required Behavior For Ticket Executor

Input:

```text
latest_ticket.json
```

Use ticket fields:

- `status`
- `symbol`
- `side`
- `qty`
- `entry_reference`
- `stop`
- `take_profit`
- `parent_order`
- `protective_stop`
- `take_profit_order`

Map to IBKR bracket:

- Parent:
  - BUY for LONG
  - SELL for SHORT only if explicitly allowed; default reject SHORT for 273 USD config
  - use LMT at `entry_reference` for first implementation
- Take-profit child:
  - opposite action
  - LMT at `take_profit`
- Stop child:
  - opposite action
  - STP at `stop`
- Use `parentId`
- Only last child transmits when not what-if
- For what-if mode, use IBKR `whatIf=True`

Set on all orders:

```python
order.eTradeOnly = False
order.firmQuoteOnly = False
```

## Create A Test Ticket First

If there is no ready ticket, generate one with demo config:

```powershell
python -m mlt.cli signal --bars data\sample_low_price_etf_ohlcv.csv --symbol US_STOCK_OR_ETF_1_SHARE_TEMPLATE --config config.live_guarded_273_usd_ibkr.json --contracts contracts.example.json --state account_state_273_usd.example.json --out runs\ibkr_273_ready_ticket
```

If that rejects, use paper demo config:

```powershell
python -m mlt.cli signal --bars data\sample_low_price_etf_ohlcv.csv --symbol US_STOCK_OR_ETF_1_SHARE_TEMPLATE --config config.paper_demo_acceptance.json --contracts contracts.example.json --state account_state_273_usd.example.json --out runs\paper_demo_signal
```

For actual IBKR paper execution, replace template symbol with a real IBKR US
stock/ETF symbol such as `AAPL` in a test ticket or use a dedicated temporary
ticket. Do not confuse template symbols with broker-tradable symbols.

## Acceptance Criteria

Minimum:

```powershell
python -m unittest discover -s tests
python broker_adapters\ibkr_readonly_probe.py --config config.ibkr_paper.template.json --out runs\accept_readonly --timeout 10
python broker_adapters\ibkr_paper_order_probe.py --config config.ibkr_paper.template.json --out runs\accept_whatif --timeout 10 --client-id 203
```

For new executor:

```powershell
python broker_adapters\ibkr_paper_ticket_executor.py --ticket <READY_TICKET_JSON> --config config.ibkr_paper.template.json --what-if --client-id 204
```

Expected:

- connects to paper port
- verifies DU account
- refuses non-READY ticket
- refuses live port
- refuses missing stop
- validates bracket order through IBKR paper what-if path
- writes JSON output under `runs\...`

Only after what-if works:

```powershell
python broker_adapters\ibkr_paper_ticket_executor.py --ticket <READY_TICKET_JSON> --config config.ibkr_paper.template.json --transmit --confirm-paper-order --client-id 205
python broker_adapters\ibkr_readonly_probe.py --config config.ibkr_paper.template.json --out runs\after_transmit_check --timeout 10
```

Expected:

- paper order appears in TWS Paper or is submitted/cancellable
- no unexpected real/live order
- open orders and positions are logged after the test

## Do Not Waste Time On

- live trading
- market data subscriptions
- strategy tuning
- options
- futures
- crypto
- automatic stock picking
- UI

The only next useful step is:

```text
ticket JSON -> IBKR Paper bracket order executor
```

