---
name: a-share-analysis
description: Analyze mainland China A-share stocks with market-specific rules, fundamentals, technical structure, policy, capital flows and event risk. Use for 沪深北交所个股分析、A股筛选、持仓复盘、买卖计划和红黄绿灯判断。
version: 1.0.0
---

# A-Share Analysis

## Scope

Cover Shanghai, Shenzhen and Beijing listed equities. Treat all conclusions as research outputs, not live-order instructions.

## Market Rules

Always identify the board before analysis:

- Main board: normally 10% daily price limit.
- STAR Market and ChiNext: normally 20% daily price limit.
- ST risk-warning stocks: apply the current exchange-specific limit and verify it.
- Beijing Stock Exchange: verify current rules before quoting a limit.
- A-shares use T+1 stock settlement for ordinary cash equities.
- Include suspension, delisting, lock-up expiry and low-liquidity risk.

Never assume rules from memory when current exchange notices can be checked.

## Data Priority

1. Exchange announcements and CNINFO filings.
2. Company annual, interim and quarterly reports.
3. SSE, SZSE, BSE and CSRC materials.
4. Audited financial databases and reputable market-data providers.
5. News and social platforms only as secondary evidence.

Every current figure needs a date.

## Workflow

### 1. Identity and board

Report code, name, exchange, board, industry, major concepts, market capitalization, free-float capitalization and liquidity.

### 2. Business and industry

Explain:

- What the company sells.
- Revenue and profit composition.
- Position in the industry chain.
- Customers, suppliers and concentration.
- Industry cycle and policy sensitivity.
- Competitive advantage and substitution risk.

### 3. Financial quality

Review at least three years when available:

- Revenue and attributable net-profit growth.
- Deducted non-recurring net profit.
- Gross and net margins.
- ROE and ROIC.
- Operating cash flow and free cash flow.
- Debt, interest burden and liquidity.
- Receivables, inventory, contract assets and goodwill.
- Related-party transactions and non-recurring gains.

Flag when profit growth is not supported by cash flow.

### 4. Valuation

Use suitable methods rather than one universal ratio:

- PE and PEG for established profitable growth.
- PB and ROE for financials or asset-heavy businesses.
- PS only when margins and path to profitability are explicit.
- EV/EBITDA where capital structure comparison matters.
- DCF or reverse DCF for scenario analysis.

Compare current valuation with the company's history and relevant A-share peers.

### 5. Technical structure

Analyze the timeframe matching the user's horizon:

- Trend and moving-average structure.
- Volume-price confirmation.
- Major support and resistance.
- Gap, limit-up and limit-down behavior.
- Turnover, volatility and liquidity.
- RSI, MACD, KDJ or Bollinger Bands only as supporting evidence.

Do not treat one indicator as a standalone signal.

### 6. Capital and ownership

Check when available:

- Major shareholders and changes.
- Institutional and fund ownership.
- Shareholder-count trend.
- Northbound holdings where applicable.
- Margin financing.
- Buybacks, placements, unlocks and insider reductions.
- Dragon-Tiger List only as short-term behavioral evidence.

### 7. Policy and catalysts

List policy, earnings, orders, product launches, restructurings, litigation, lock-up expiries and other dated events. Separate confirmed announcements from market rumors.

### 8. Risk and decision

Return:

- Bull thesis.
- Strongest bear thesis.
- Key data that can falsify each thesis.
- Valuation range with assumptions.
- Technical levels and thesis-invalidation level.
- Liquidity and gap risk.
- GREEN / YELLOW / RED / DATA_BLOCKED status.

## Output Minimum

- Exact code, board and timestamp.
- Three strongest positive facts.
- Three strongest negative facts.
- Financial-quality conclusion.
- Valuation conclusion.
- Technical structure.
- Upcoming events.
- Invalidation conditions.
- Sources.
