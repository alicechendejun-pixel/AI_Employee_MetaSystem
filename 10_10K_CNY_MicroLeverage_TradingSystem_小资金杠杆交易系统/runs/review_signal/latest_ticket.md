# Manual Order Ticket

Status: REJECTED
Symbol: SAMPLE_FUT
Signal date: 2026-02-20
Side: LONG
Quantity: 0
Entry reference: 112.0
Stop: 104.0
Take profit: 128.0

## Risk
Capital: 10000.0
Risk budget: 50.0
Risk per contract: 112.0
Margin required: 0.0

## Checklist
- Broker contract symbol exactly matches this ticket.
- Multiplier, tick size, commission, and margin match broker screen.
- Stop order is entered at the same time as the entry order.
- No trade is placed if daily loss or drawdown kill switch is active.
- No trade is placed during limit-up/limit-down, illiquid, or abnormal spread conditions.

Reject reason: risk_budget_too_small

Reason: close 112.0000 broke previous 10-bar high 111.0000
