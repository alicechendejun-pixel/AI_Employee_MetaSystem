---
name: stock-question-refiner
description: Convert an informal stock question into a precise research brief for A-share, Hong Kong or US equity analysis. Use before deep due diligence, comparisons, backtests or position reviews when the request lacks explicit scope, horizon or decision criteria.
version: 1.0.0
---

# Stock Question Refiner

## Purpose

Transform a vague request into a structured brief without changing the user's objective or inventing portfolio facts.

## Required Brief

Produce:

- Market, ticker and company.
- Security type and exchange.
- Decision being considered.
- Holding horizon.
- Current position and cost, only when supplied.
- Maximum acceptable risk, only when supplied.
- Investment style: growth, value, cyclical, event-driven, turnaround, income or trading.
- Priority questions.
- Required current data.
- Comparison group or benchmark.
- Known constraints.
- Missing information and assumptions.

## Research Modes

Choose one or combine explicitly:

1. Quick factual check.
2. Fundamental analysis.
3. Technical and trading-structure analysis.
4. Full eight-phase due diligence.
5. Peer comparison.
6. Position review.
7. Entry or exit scenario planning.
8. Rule-based backtest.

## Refinement Rules

- Preserve the user's ticker, market and horizon.
- Convert relative dates into exact dates.
- Separate research questions from desired conclusions.
- Do not assume account size, cost basis or risk tolerance.
- Mark unsupported assumptions.
- Require current verification for price, filings, news, rules and event dates.
- For backtests, force exact entry, exit, universe, benchmark, costs and sample period.

## Output Template

```markdown
# Research Brief

## Instrument
- Market:
- Ticker / company:
- Security type:

## Decision
- User objective:
- Horizon:
- Current position information:
- Risk constraint:

## Priority Questions
1.
2.
3.

## Required Workstreams
- Market-specific analysis:
- Fundamental and valuation:
- Technical structure:
- Events and positioning:
- Bear case:
- Backtest:
- Risk review:

## Required Fresh Data
- Price timestamp:
- Latest filing period:
- Upcoming events:
- Market-rule verification:

## Assumptions and Gaps
- Confirmed facts:
- Assumptions:
- Missing information:

## Deliverable
- Status system: GREEN / YELLOW / RED / DATA_BLOCKED
- Required tables and scenarios:
- Sources and dates required:
```

## Handoff

Pass the completed brief to `stock-research-executor`, then to the market adapter, backtest module and risk manager as required.
