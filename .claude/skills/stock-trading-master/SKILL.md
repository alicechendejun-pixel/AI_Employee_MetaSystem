---
name: stock-trading-master
description: Unified A-share, Hong Kong and US stock research, deep due diligence, technical analysis, backtesting and portfolio risk-control orchestrator. Use for stock evaluation, comparisons, signal validation, trading plans, red-yellow-green ratings and post-trade review. Research and simulation only; no live orders.
version: 1.1.1
---

# Stock Trading Master System

## Mission

Turn a stock question into a dated, sourced and risk-controlled decision package by coordinating independent market, research, backtest and risk modules.

## Market routing

- **A-share:** use `a-share-analysis`; account for T+1, board-specific price limits, suspensions, ST rules, policy and liquidity.
- **Hong Kong:** use `hong-kong-stock-analysis`; account for T+2 settlement, board and odd lots, Stock Connect, AH/ADR structure, auction/VCM rules, stamp duty, governance and liquidity.
- **US:** use `us-stock-analysis`; account for T+1 settlement, SEC filings, extended hours, earnings gaps, ownership, options-implied volatility and currency exposure.

Then use:

1. `stock-question-refiner` to standardize the question.
2. `stock-research-executor` for eight-phase due diligence.
3. `backtesting-trading-strategies` when rules are explicit.
4. `risk-manager` as the final veto layer.

Native core skills live in `.claude/skills/`. Optional third-party enhancements are registered in `config/upstreams.json`.

## Required request fields

Infer available information and clearly record:

- Market, ticker and company.
- Objective: analysis, comparison, entry plan, position review, screening or backtest.
- Horizon: intraday, swing, medium term or long term.
- Position, cost and maximum risk when supplied.
- Missing assumptions and unresolved uncertainties.

## Workflow

### 1. Freshness gate

Verify current price timestamp, latest completed reporting period, exchange filings, corporate actions, material news and upcoming events. Use `DATA_BLOCKED` when critical current information cannot be verified.

### 2. Independent evidence streams

Produce separate evidence summaries for:

- Fundamentals and valuation.
- Technical and market structure.
- Events and catalysts.
- Bear case, accounting and governance risk.

Do not let one stream inherit another stream's conclusion before collecting its own evidence.

### 3. Cross-validation

Check:

- Net income against operating cash flow.
- Revenue growth against receivables and inventory.
- Company metrics against peers and history.
- Price trend against volume and market breadth.
- Thesis against dated falsification events.
- Strategy edge after realistic costs.
- Cross-listed prices after currency, conversion ratio, share class, liquidity and fungibility limits.

### 4. Backtest gate

For rule-based strategies report universe, date range, entry and exit rules, benchmark, trade count, win rate, payoff ratio, expectancy, annualized return, maximum drawdown, risk-adjusted return, costs, taxes, slippage and sample-out results.

Reject look-ahead bias, survivorship bias, unrealistic fills and parameter tuning on the whole sample. For Hong Kong include board lots, odd-lot execution, stamp duty, levies, suspensions, corporate actions and Stock Connect constraints.

### 5. Risk veto

Evaluate position risk, portfolio concentration, factor overlap, liquidity, gap risk, event risk, thesis invalidation and stress loss. Provide both a price-risk control and a thesis-invalidation condition. Risk may veto a positive research score.

### 6. Synthesis

Use `references/output-schema.md` and return one status:

- `GREEN`: current and consistent evidence, acceptable risk, no veto.
- `YELLOW`: mixed evidence, event uncertainty, weak robustness or incomplete data.
- `RED`: thesis failure, unacceptable risk, poor evidence or failed backtest.
- `DATA_BLOCKED`: critical information unavailable or stale.

## Scoring

Score 0–5 for business quality, financial quality, valuation, industry/catalysts, technical structure, evidence quality, strategy robustness and risk-adjusted attractiveness.

- Short swing: emphasize technicals, events, robustness and risk.
- Medium term: balance business, financials, valuation, catalysts and technicals.
- Long term: emphasize business, financials, valuation and risk.

A critical risk veto overrides the weighted score.

## Evidence order

1. Exchange and regulatory filings.
2. Company investor-relations materials.
3. Government and industry data.
4. Reputable market-data providers.
5. Credible journalism and analyst research.
6. Social media only as a lead, never sole proof.

Separate fact, inference and scenario. Give every material factual claim a source and date.

## Optional upstream location

The optional installer stores upstream repositories under:

`03_Wealth_Trading_搞钱与交易/A股港股美股交易评测系统/vendor/`

The installer itself is:

`03_Wealth_Trading_搞钱与交易/A股港股美股交易评测系统/scripts/install_upstreams.ps1`

## Invocation examples

- `/stock-trading-master analyze 688010 福光股份 medium-term`
- `/stock-trading-master analyze 00700 腾讯控股 market=Hong-Kong horizon=6m`
- `/stock-trading-master compare 09988 BABA cross-listing=true horizon=6-12m`
- `/stock-trading-master compare NVDA AMD horizon=6-12m`
- `/stock-trading-master backtest "20-day breakout with ATR stop" universe=HSI`

## Non-negotiable output

- Exact market and ticker.
- Data timestamp and latest reporting period.
- Primary thesis and strongest counter-thesis.
- Valuation range or key technical levels with assumptions.
- Catalysts and explicit invalidation conditions.
- Risk budget and stress case.
- GREEN / YELLOW / RED / DATA_BLOCKED with reasons.
- Source list and module trace.
- No fabricated precision.
- No broker credentials or live order placement.
