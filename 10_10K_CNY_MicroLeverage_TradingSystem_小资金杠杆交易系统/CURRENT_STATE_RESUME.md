# Current State Resume

Last updated: 2026-05-28

## Resume Point

Continue from:

```text
G:\我的云端硬盘\09-AI员工系统\10K_CNY_MicroLeverage_TradingSystem_小资金杠杆交易系统
```

Read first:

```text
HANDOFF_TO_CLAUDE_OPUS_4_7.md
IBKR_PAPER_TRADING_PLAN.md
IBKR_273_USD_LIVE_READINESS.md
```

## What Is Already Done

- Local trading/risk/ticket system exists.
- IBKR `ibapi` was installed in Python 3.11.
- TWS Paper socket was reachable at `127.0.0.1:7497`.
- Paper account was read as `DUE972820`.
- Read-only probe succeeded.
- Paper what-if order probe succeeded for AAPL 1 share limit order.
- Deprecated ibapi flags fixed:
  - `order.eTradeOnly = False`
  - `order.firmQuoteOnly = False`
- No positions and no open orders were left after probes.

## Important TWS Settings

In TWS Paper:

- `Enable ActiveX and Socket Clients`: enabled
- Port: `7497`
- `Read-Only API`: must be OFF for order-write tests
- Account must start with `DU`

## Commands To Recheck After Reboot

Start TWS and log into Paper Trading first. Then run:

```powershell
cd "G:\我的云端硬盘\09-AI员工系统\10K_CNY_MicroLeverage_TradingSystem_小资金杠杆交易系统"
python broker_adapters\ibkr_readonly_probe.py --config config.ibkr_paper.template.json --out runs\ibkr_readonly_probe --timeout 10
python broker_adapters\ibkr_paper_order_probe.py --config config.ibkr_paper.template.json --out runs\ibkr_paper_order_probe_whatif --timeout 10 --client-id 189
```

## Next Task

Implement:

```text
broker_adapters\ibkr_paper_ticket_executor.py
```

Goal:

```text
latest_ticket.json -> IBKR Paper bracket order
```

Keep all safety rules from `HANDOFF_TO_CLAUDE_OPUS_4_7.md`.

