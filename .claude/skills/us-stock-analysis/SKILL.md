---
name: us-stock-analysis
description: Analyze US-listed equities through fundamentals, valuation, technical structure, earnings, institutional ownership and event risk. Use for US stock research, ticker comparisons, position reviews, entry plans and red-yellow-green decisions.
version: 1.0.0
---

# US Stock Analysis

## Scope

Analyze NYSE, Nasdaq and other US-listed equities. State whether the security is a common stock, ADR, ETF, closed-end fund, SPAC or another structure.

## Freshness Gate

Verify:

- Current or latest completed-session price.
- Market session and timezone.
- Latest 10-K, 10-Q, 8-K and earnings release.
- Upcoming earnings date.
- Material corporate actions and recent news.

Return `DATA_BLOCKED` when critical current data cannot be verified.

## Source Priority

1. SEC filings and exchange notices.
2. Company investor-relations materials.
3. Government and regulatory data.
4. Reputable market-data providers.
5. Credible financial journalism and clearly identified analyst research.

## Workflow

### 1. Company and security structure

Report ticker, exchange, company, sector, industry, market cap, enterprise value, share classes, ADR ratio when relevant and material dilution instruments.

### 2. Business quality

Analyze:

- Revenue and profit drivers.
- Recurring versus cyclical revenue.
- Customer and supplier concentration.
- Competitive advantage and switching costs.
- Total addressable market only when supported by a source.
- Management execution and capital allocation.

### 3. Financial quality

Review three to five years when available:

- Revenue, EPS and free-cash-flow growth.
- Gross, operating and net margins.
- ROIC and ROE.
- Stock-based compensation and dilution.
- Net cash or debt, interest coverage and maturity profile.
- Operating cash flow versus net income.
- Working-capital changes.
- Buybacks, dividends and acquisitions.

Flag aggressive non-GAAP adjustments and weak cash conversion.

### 4. Valuation

Select methods suitable for the business:

- Forward and trailing PE.
- EV/EBITDA and EV/FCF.
- Price-to-sales with explicit margin assumptions.
- PEG with caution around cyclicality.
- DCF, reverse DCF or scenario analysis.

Compare with historical ranges and direct peers. State all growth, margin and discount-rate assumptions.

### 5. Earnings and expectations

Distinguish business results from expectation changes:

- Revenue and EPS surprise.
- Guidance versus consensus.
- Estimate revisions.
- Segment and geographic trends.
- Management commentary.
- Implied move and realized move when options data is relevant.

### 6. Technical structure

Use the user's horizon:

- Trend and 20/50/200-day moving-average structure.
- Relative strength versus sector and benchmark.
- Volume, gaps and volatility.
- Support, resistance and invalidation levels.
- RSI, MACD and other indicators only as confirmation.

### 7. Ownership and positioning

Check when material:

- Institutional ownership and 13F changes.
- Insider transactions.
- Short interest and days to cover.
- Options skew, open interest and unusual concentration.
- ETF and index inclusion effects.

Treat delayed 13F data as historical, not real-time positioning.

### 8. Catalysts and risks

List dated catalysts and failure modes:

- Earnings.
- Product or regulatory decisions.
- Litigation.
- Financing and dilution.
- Lock-up expiry.
- Macro and currency exposure.
- Customer concentration.
- Competitive disruption.

### 9. Synthesis

Return:

- Primary thesis.
- Strongest bear case.
- Valuation range.
- Technical structure.
- Upcoming catalysts.
- Thesis and price invalidation.
- GREEN / YELLOW / RED / DATA_BLOCKED.

## Comparison Mode

For two or more tickers, use the same period and accounting basis. Compare business quality, growth, cash conversion, balance sheet, valuation, revisions, technical relative strength and risk-adjusted attractiveness.

## Output Minimum

- Ticker, session and timestamp.
- Latest filing period.
- Key financial and valuation table.
- Bull and bear cases.
- Earnings expectation view.
- Technical levels.
- Catalysts and invalidation.
- Sources.
