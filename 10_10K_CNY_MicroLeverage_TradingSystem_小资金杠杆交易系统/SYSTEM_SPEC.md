# System Specification

## Name

10K CNY Micro Leverage Trading System.

## Objective

Provide a local, auditable, risk-first workflow for a 10,000 CNY small-capital
account that wants to research and manually execute high-leverage trades only
after risk controls have approved the ticket.

## Supported Asset Classes

The engine is generic and can model any linear instrument with:

- OHLCV bars
- contract multiplier
- tick size
- margin rate
- commission per contract

This covers many futures-like products and can also be adapted to ETFs, stocks,
or CFDs by setting multiplier and margin appropriately. Real tradability depends
on the user's broker and account permissions.

## Data Contract

Input CSV columns:

```text
date,open,high,low,close,volume
```

The file must be chronological. Adjusted continuous futures series are allowed
for research, but live tickets must use the currently tradable contract symbol
and exact broker contract specs.

## Strategy

Default strategy: Donchian breakout plus ATR stop.

- Long signal: latest close breaks the previous `entry_lookback` high and is
  above the SMA trend filter.
- Short signal: latest close breaks the previous `entry_lookback` low and is
  below the SMA trend filter.
- Stop: `ATR * atr_stop_multiple` from entry reference.
- Take profit: `take_profit_r_multiple` times stop risk.

## Risk Sizing

For each signal:

```text
risk_budget = current_equity * risk_per_trade_fraction
stop_risk = abs(entry - stop) * multiplier
slippage_risk = 2 * slippage_ticks * tick_size * multiplier
fee_risk = 2 * commission_per_contract
risk_per_contract = stop_risk + slippage_risk + fee_risk
qty_by_risk = floor(risk_budget / risk_per_contract)
qty_by_margin = floor((equity * max_margin_fraction - open_margin) / margin_per_contract)
qty = min(qty_by_risk, qty_by_margin)
```

If `qty < min_qty`, the ticket is rejected.

## Kill Switches

The signal command accepts `--state account_state.example.json`.

Fields:

- `current_equity`
- `peak_equity`
- `realized_pnl_today`
- `open_margin`

The engine rejects new tickets if:

- daily realized loss exceeds `max_daily_loss_fraction`
- total drawdown from peak exceeds `max_total_drawdown_fraction`

## Output Contract

The signal command writes:

- `latest_ticket.json`
- `latest_ticket.md`

Ticket includes:

- status: `READY` or `REJECTED`
- symbol
- side
- quantity
- entry reference
- stop
- take profit
- parent order instruction
- protective stop instruction
- risk budget
- risk per contract
- margin required
- human review checklist

## Execution Boundary

This MVP produces manual order tickets only. Broker API execution is not
implemented. This is deliberate. Live execution needs separate fill tracking,
order reconciliation, cancellation handling, connection recovery, and broker
permission checks.

## API Boundary

The current codebase uses no broker API.

It does not call IBKR TWS API, IBKR Client Portal API, or any other broker API.
`broker_adapters/` and `IBKR_PAPER_TRADING_PLAN.md` define the future adapter
boundary only.
