# Risk Disclosure

This system is software, not a promise of profit.

Small-capital leveraged trading is structurally fragile:

- One normal stop can be a large percentage of a 10,000 CNY account.
- Futures margin is not the maximum loss.
- A gap can fill beyond the stop price.
- Intraday liquidity can disappear.
- Exchange limits can prevent timely exit.
- Broker margin rules can change without warning.
- Data errors can produce false signals.
- Backtest performance can fail in live trading.

The default config is guarded:

- 0.5% risk per trade
- 35% maximum margin use
- 1.5% daily loss stop
- 8% total drawdown stop
- manual ticket only

If these limits reject a trade, the system is doing its job.

No file in this folder selects a real tradable instrument for the user. Real
instrument selection, contract verification, account permissions, and final order
entry remain the operator's responsibility.

