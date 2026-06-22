---
name: backtesting-trading-strategies
description: Design and evaluate rule-based trading backtests for A-share, Hong Kong and US markets. Use when a strategy has explicit entry, exit, universe and risk rules, or when a trading signal needs historical validation.
version: 1.1.0
---

# Backtesting Trading Strategies

## Entry Gate

Do not backtest a vague idea. First define:

- Market and tradable universe.
- Data frequency and date range.
- Exact entry rule.
- Exact exit rule.
- Position sizing.
- Rebalancing schedule.
- Benchmark.
- Fees, taxes and slippage.
- Corporate-action handling.

Return `RULES_INCOMPLETE` when the strategy cannot be reproduced from the specification.

## Market Constraints

### A-share

Model T+1 sell restrictions, board-specific price limits, suspensions, ST status, delistings, lot size, transaction costs and unavailable fills at locked limit-up or limit-down prices.

### Hong Kong

Model:

- T+2 settlement assumptions where they affect cash reuse or portfolio accounting.
- Board-lot sizing and separate odd-lot execution quality.
- Current Hong Kong stock stamp duty, exchange levies, brokerage, platform fees and slippage.
- Suspensions, delistings, prolonged trading halts and low-free-float securities.
- Closing Auction Session and Volatility Control Mechanism applicability.
- Rights issues, placements, share consolidations, special dividends, spin-offs and other corporate actions.
- Stock Connect eligibility and trading calendars when the strategy is intended for southbound execution.
- Survivorship changes in Hang Seng and other Hong Kong index universes.
- Currency conversion and ADR/AH conversion assumptions in cross-listed strategies.

Do not treat AH or ADR price differences as freely arbitrageable without modelling conversion, fungibility, funding and trading constraints.

### US

Model splits, dividends, delistings, survivorship, extended-hours assumptions, borrow availability for shorts, commissions and realistic market impact.

## Bias Controls

Reject or flag:

- Look-ahead bias.
- Survivorship bias.
- Selection after seeing outcomes.
- Use of revised fundamentals before publication dates.
- Same-bar signal and fill without a justified execution model.
- Unrealistic fills during gaps, auctions, suspensions or price-limit locks.
- Parameter tuning on the full sample.

## Test Design

Use:

1. Development or in-sample period.
2. Validation period.
3. Final out-of-sample period.
4. Walk-forward or rolling tests when data permits.
5. Sensitivity tests around major parameters.
6. Stress tests with higher costs and worse fills.

## Required Metrics

Report:

- Trade count.
- Win rate.
- Average win and average loss.
- Payoff ratio.
- Expectancy per trade.
- Total and annualized return.
- Maximum drawdown and drawdown duration.
- Volatility.
- Sharpe or another stated risk-adjusted measure.
- Exposure and turnover.
- Best and worst periods.
- Benchmark-relative return.

## Robustness Tests

Check:

- Neighboring parameter values.
- Different market regimes.
- Subperiod consistency.
- Sector and size concentration.
- Dependence on a small number of trades.
- Cost, tax and slippage sensitivity.
- Entry-delay sensitivity.
- Liquidity and universe-membership sensitivity.

## Decision

Return one of:

- `PASS`: out-of-sample edge remains after realistic costs and robustness checks.
- `CONDITIONAL`: some evidence of edge, but concentration, regime dependence or limited sample remains.
- `REJECTED`: no reliable out-of-sample edge or material bias.
- `DATA_BLOCKED`: required historical data is unavailable or unreliable.

## Output Template

- Strategy specification.
- Data and universe.
- Execution assumptions.
- Bias audit.
- Performance table.
- Drawdown analysis.
- In-sample versus out-of-sample comparison.
- Robustness and stress results.
- Failure modes.
- PASS / CONDITIONAL / REJECTED / DATA_BLOCKED.
