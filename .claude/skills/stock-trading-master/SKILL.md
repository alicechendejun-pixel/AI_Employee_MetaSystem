---
name: stock-trading-master
description: Unified A-share, Hong Kong and US stock research, technical analysis, deep due diligence, backtesting and portfolio risk-control orchestrator. Use for individual-stock research, market comparisons, signal validation, trading plans, red-yellow-green ratings, event monitoring and post-trade review. This skill is analysis-first and must not place live orders unless a separately reviewed execution adapter is explicitly enabled.
version: 1.1.0
---

# Stock Trading Master System

## Mission

Convert a stock-related request into a traceable, evidence-based decision package by coordinating specialized market and research skills instead of relying on one model opinion.

The system combines five layers:

1. **Market adapter**: China A-share, Hong Kong or US-stock specialist.
2. **Institutional research**: eight-phase due diligence and source grading.
3. **Technical and event analysis**: trend, levels, earnings and positioning checks.
4. **Strategy validation**: historical backtest and robustness checks.
5. **Risk governor**: position sizing, stop conditions, concentration and portfolio-risk vetoes.

## Safety Boundary

- Default mode is **research / simulation / paper trading only**.
- Never submit a live order, expose an API key, or modify broker configuration through this skill.
- A trade idea is not approved merely because one module produces a bullish signal.
- Missing, stale or contradictory data must downgrade confidence.
- Always state the data timestamp and market session.
- For A-shares, account for T+1, board-specific price limits, suspension risk, ST rules and liquidity.
- For Hong Kong stocks, account for T+2 settlement, board lots and odd lots, Stock Connect eligibility, auction and VCM rules, stamp duty, cross-listing structure and liquidity.
- For US stocks, account for T+1 settlement, extended hours, earnings gaps, options-implied volatility and currency exposure when relevant.

## Required Inputs

Infer what is available and ask only when execution would otherwise be materially wrong:

- Market: A-share / Hong Kong / US.
- Ticker and company name.
- Objective: research, screening, entry plan, position review, exit review, comparison or backtest.
- Time horizon: intraday, swing, medium term or long term.
- Current position, cost and intended maximum risk, when supplied.

## Routing Map

Read `config/upstreams.json` for the optional upstream source registry. Prefer the native skills in `.claude/skills/` for the core workflow.

### A-share

Use `a-share-analysis` for market-specific fundamentals, technicals, policy impact, capital flow and trading rules. Add `a-share-screener` for candidate selection and `akshare` when structured China-market data access is needed. Then pass conclusions to the deep-research and risk layers.

### Hong Kong stocks

Use `hong-kong-stock-analysis` for HKEX-specific fundamentals, valuation, governance, board-lot and odd-lot liquidity, T+2 settlement, Stock Connect, AH/ADR or dual-listing comparisons, stamp-duty-aware return assumptions, corporate actions and market structure. Then pass conclusions to the deep-research, backtest and risk layers.

### US stocks

Use `us-stock-analysis` for financials, valuation, technical structure and peer comparison. Add `earnings-calendar`, `institutional-flow-tracker` and `options-strategy-advisor` only when relevant.

### Deep due diligence

Use `stock-question-refiner` to normalize the question and `stock-research-executor` for the eight-phase process:

1. Business foundation.
2. Industry cycle.
3. Business breakdown.
4. Financial quality.
5. Ownership and governance.
6. Market disagreement.
7. Valuation and moat.
8. Final synthesis.

### Backtest

Use `backtesting-trading-strategies` only after the trading rule is explicit. Reject tests with look-ahead bias, survivorship bias, insufficient sample size, unrealistic fills or unreported costs.

For Hong Kong tests, include board lots, odd-lot execution, stamp duty, transaction levies, T+2 settlement assumptions, suspensions, corporate actions, Stock Connect eligibility where relevant and realistic liquidity.

### Risk governor

Use `risk-manager` last. Risk can veto a trade even when research and technical signals are positive.

## Standard Workflow

### Stage 0 — Request normalization

Create a compact research brief:

- Instrument and market.
- Decision horizon.
- User question.
- Required fresh data.
- Known position constraints.
- Uncertainties.

### Stage 1 — Freshness gate

Collect current price, latest completed financial period, relevant filings, corporate actions, material news and upcoming events. Mark each item with date and source.

Stop and return `DATA_BLOCKED` when critical data cannot be verified.

### Stage 2 — Independent analyses

Run these streams independently where tooling permits:

- Fundamental and valuation stream.
- Technical and market-structure stream.
- Event / catalyst stream.
- Bear-case and fraud / governance stream.

Do not let one stream see another stream's conclusion before producing its own evidence summary.

### Stage 3 — Cross-validation

Check at minimum:

- Net income versus operating cash flow.
- Revenue growth versus receivables and inventory.
- Company metrics versus peers and its own history.
- Price trend versus volume and breadth.
- Thesis versus upcoming events that can falsify it.
- Claimed edge versus backtest after costs.
- For cross-listed securities, price and valuation differences after currency, conversion ratio, share class, liquidity and fungibility constraints.

### Stage 4 — Backtest gate

For rule-based signals, report:

- Universe and date range.
- Entry and exit rules.
- Benchmark.
- Number of trades.
- Win rate, payoff ratio and expectancy.
- CAGR or annualized return.
- Maximum drawdown.
- Sharpe or a clearly stated alternative.
- Transaction costs, taxes and slippage assumptions.
- In-sample and out-of-sample split.

A strategy with strong in-sample results but weak out-of-sample results is `REJECTED`.

### Stage 5 — Risk veto

Evaluate:

- Position risk in currency and percentage terms.
- Portfolio concentration and factor overlap.
- Liquidity and gap risk.
- Event risk.
- Stop invalidation logic.
- Expected loss under ordinary and stress scenarios.

Never substitute a percentage stop for a thesis-invalidation condition; provide both when possible.

### Stage 6 — Synthesis

Use the output schema in `references/output-schema.md`.

Final status:

- `GREEN`: evidence is consistent, data is current, risk is acceptable and no veto remains.
- `YELLOW`: mixed evidence, event uncertainty, weak robustness or incomplete data.
- `RED`: thesis failure, unacceptable risk, poor data quality or backtest rejection.
- `DATA_BLOCKED`: critical information unavailable or stale.

## Scoring Framework

Score each dimension from 0 to 5:

- Business quality.
- Financial quality.
- Valuation.
- Industry / catalyst structure.
- Technical structure.
- Evidence quality.
- Strategy robustness.
- Risk-adjusted attractiveness.

Weights depend on horizon:

- Intraday / short swing: technical 25%, event 20%, robustness 20%, risk 25%, remaining 10%.
- Medium term: business 15%, financial 15%, valuation 15%, industry/event 15%, technical 15%, evidence 10%, robustness 5%, risk 10%.
- Long term: business 20%, financial 20%, valuation 20%, industry 10%, evidence 10%, risk 15%, technical 5%.

A single critical veto overrides the weighted score.

## Evidence Rules

Prioritize:

1. Regulatory filings and exchange announcements.
2. Company investor-relations materials.
3. Government and industry data.
4. Reputable market-data providers.
5. Credible journalism and analyst research.
6. Social media only as a lead, never as sole proof.

Every material factual claim needs a source and date. Clearly separate fact, inference and scenario.

## Invocation Examples

- `/stock-trading-master analyze 688010 福光股份 medium-term`
- `/stock-trading-master analyze 00700 腾讯控股 medium-term market=Hong-Kong`
- `/stock-trading-master compare 09988 BABA 6-12m cross-listing=true`
- `/stock-trading-master compare NVDA AMD 6-12m`
- `/stock-trading-master review-position 000625 cost=18.40`
- `/stock-trading-master backtest "20-day breakout with ATR stop" universe=HSI`
- `/stock-trading-master daily-signal market=A-share`

## Local Upstream Discovery

The optional installer places upstream repositories under:

`03_Wealth_Trading_搞钱与交易/StockTradingMaster/vendor/`

Before using an optional module:

1. Read its `SKILL.md`.
2. Follow its own references only as needed.
3. Record which upstream module contributed each conclusion.
4. Fall back to the native market and research skills when an upstream module is unavailable.

## Non-Negotiable Output Requirements

- Exact market and ticker.
- Data timestamp.
- Primary thesis and strongest counter-thesis.
- Key levels or valuation ranges with assumptions.
- Explicit invalidation conditions.
- Risk budget, not only upside target.
- Red / yellow / green status with reasons.
- Source list.
- No fabricated precision.
