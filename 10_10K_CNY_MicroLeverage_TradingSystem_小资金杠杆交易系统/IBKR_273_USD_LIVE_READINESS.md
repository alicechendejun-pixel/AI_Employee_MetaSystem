# IBKR 273 USD Live Readiness

## Direct Answer

Yes, a 273 USD IBKR account can potentially place real trades, but the suitable
scope is narrow:

```text
US stocks / US ETFs, long-only, small whole-share or fractional-size positions.
```

The unsuitable starting scope is:

```text
futures, options, short selling, margin leverage, high-frequency day trading.
```

## API Cost

The IBKR TWS API itself is not the main cost item. The practical costs are:

- market data subscriptions if you need live or API historical data
- commissions and regulatory/exchange fees
- bid/ask spread and slippage

IBKR documentation states that real-time top-of-book, depth, and historical data
through the API require live market data subscriptions for the instruments.
IBKR's scanner API can be used without market data fields, but that is not a
replacement for tradable quotes.

## Current System API Status

This system still does not call IBKR API.

For the 273 USD account, use it now as:

- local CSV backtest
- local universe screen
- manual ticket generator
- future IBKR Paper adapter specification

Do not assume it can submit orders to IBKR until the adapter is implemented and
paper-tested.

## Added Guarded Config

Use:

```text
config.live_guarded_273_usd_ibkr.json
account_state_273_usd.example.json
universe.ibkr_273_usd_start.json
```

Run:

```powershell
python -m mlt.cli screen --universe universe.ibkr_273_usd_start.json --config config.live_guarded_273_usd_ibkr.json --contracts contracts.example.json --state account_state_273_usd.example.json --out runs\ibkr_273_screen
```

Only `READY` candidates may go to manual review.

## Risk Settings

The 273 USD config uses:

- 1% risk per trade = 2.73 USD
- 2% daily loss stop = 5.46 USD
- 8% total drawdown stop = 21.84 USD
- long-only
- no live broker execution

With such a small account, commissions and spread matter a lot. A trade that is
mathematically acceptable can still be economically poor if fees/spread consume
too much of the expected edge.

## Practical Recommendation

Start with IBKR Paper once the adapter exists. Until then, run local paper
workflow:

1. export/download daily bars for real US stocks/ETFs
2. update `contracts.example.json` or create `contracts.ibkr_us.json`
3. run `screen`
4. run `signal` only for READY symbols
5. manually compare the ticket with the IBKR order preview

