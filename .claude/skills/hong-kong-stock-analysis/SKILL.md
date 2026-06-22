---
name: hong-kong-stock-analysis
description: Analyze Hong Kong-listed equities with HKEX-specific trading, settlement, board-lot, Stock Connect, dual-counter, corporate-action, governance, liquidity and valuation considerations. Use for 港股分析、港股通标的、AH股比较、ADR/二次上市比较、持仓复盘、买卖计划和红黄绿灯判断。
version: 1.0.0
---

# Hong Kong Stock Analysis

## Scope

Analyze Main Board and GEM securities listed on HKEX, including H shares, red chips, P chips, local Hong Kong companies, secondary listings, dual-primary listings, REITs and eligible Stock Connect securities.

This skill is for research, simulation and paper-trading plans. It does not submit live orders.

## Freshness Gate

Before analysis, verify:

- Exact stock code, company name and security type.
- Latest completed HKEX trading session and price timestamp.
- Latest annual/interim report and current HKEX announcements.
- Current board lot, trading currency and whether a dual-counter exists.
- Stock Connect eligibility and southbound trading status when relevant.
- Upcoming results, dividends, rights issues, placements, buybacks, suspensions and other corporate actions.

Return `DATA_BLOCKED` when critical filings, trading status or current market data cannot be verified.

## HKEX Market Rules

- Normal Hong Kong Exchange Trades and Clearing Agency Transactions settle on T+2 through CCASS.
- The market is order-driven and uses board lots; odd-lot liquidity and execution can differ materially from board-lot trading.
- Hong Kong does not use the A-share-style universal daily percentage price limit. Applicable securities may instead be subject to the Volatility Control Mechanism, quotation rules and auction-session price controls.
- Closing Auction Session securities use a reference-price framework; verify whether the instrument is CAS-eligible.
- Hong Kong stock transfers are subject to current stamp-duty and exchange-related transaction costs unless exempt. Verify current rates before calculating return or backtest results.
- Southbound trading follows Stock Connect eligibility, calendars, quotas and trading arrangements, which can differ from direct Hong Kong brokerage access.
- Severe-weather trading and clearing arrangements must be verified for the relevant date.

Do not assume these rules remain unchanged; verify current HKEX and Hong Kong Government materials when the decision depends on them.

## Security Classification

Classify the company before valuation:

- H share.
- Red chip.
- P chip or other mainland private enterprise.
- Hong Kong local company.
- Secondary or dual-primary listing.
- REIT, ETF, stapled security or other structure.

Identify the controlling shareholder, incorporation jurisdiction, reporting currency and accounting standard.

## Workflow

### 1. Business and listing structure

Report:

- Stock code, board, listing type and trading currency.
- Main business, revenue and profit composition.
- Mainland, Hong Kong and overseas exposure.
- Controlling shareholder and state-owned-enterprise status when applicable.
- Any A-share, ADR or other overseas listing relationship.
- Fungibility, conversion ratio and practical arbitrage constraints where relevant.

### 2. Financial quality

Review at least three reporting periods when available:

- Revenue and attributable profit.
- Adjusted versus reported profit.
- Operating cash flow and free cash flow.
- Gross, operating and net margins.
- ROE and ROIC.
- Net cash or debt, refinancing and interest burden.
- Receivables, inventory, contract assets and goodwill.
- Dividends, payout ratio and coverage.
- Share-based compensation and dilution.

Flag weak cash conversion, repeated placements, large related-party balances and reliance on fair-value gains.

### 3. Governance and capital allocation

Review:

- Controlling shareholder and connected transactions.
- Board independence and auditor history.
- Insider purchases and disposals.
- Placements, rights issues, convertible securities and share consolidation.
- Buybacks and cancellation of repurchased shares.
- Privatisation, spin-off and restructuring probability.
- Dividend policy and capital-return record.

### 4. Valuation

Use business-appropriate methods and compare:

- Current valuation versus the company's Hong Kong history.
- Direct Hong Kong peers.
- A-share premium or discount for AH dual-listed companies.
- ADR or US-listed peer valuation where relevant.
- Dividend yield, payout sustainability and Hong Kong interest-rate sensitivity.
- Conglomerate or holding-company discount.

For AH comparisons, adjust for share count, currency, conversion ratio, liquidity, investor base and fungibility limitations. Do not treat the price gap as risk-free arbitrage.

### 5. Trading structure and liquidity

Analyze:

- Board lot and odd-lot implications.
- Average daily value traded, spread and market depth.
- Free float and controlling-shareholder concentration.
- Southbound ownership and flow where available.
- Short-selling eligibility, short interest and securities-lending constraints.
- Dual-counter HKD/RMB liquidity when applicable.
- Suspension history and gap risk.
- Closing Auction Session and Volatility Control Mechanism applicability.

### 6. Technical structure

Match the timeframe to the user's horizon:

- Primary trend and moving-average structure.
- Volume-price confirmation.
- Support, resistance and gap levels.
- Relative strength versus Hang Seng Index, Hang Seng China Enterprises Index or Hang Seng TECH Index as appropriate.
- RSI, MACD and other indicators only as supporting evidence.

### 7. Catalysts and calendar

Include dated events:

- Annual or interim results.
- Dividend declaration and ex-date.
- Mainland policy changes.
- Stock Connect inclusion or removal.
- Index rebalancing.
- Placements, rights issues, buybacks and privatisation proposals.
- A-share or ADR events affecting price discovery.
- Regulatory, litigation and audit events.

### 8. Risk review

Explicitly assess:

- Controlling-shareholder and governance risk.
- Low-float and liquidity risk.
- Placement and dilution risk.
- Currency and Hong Kong interest-rate exposure.
- Mainland policy and geopolitical exposure.
- Stock Connect flow dependence.
- Discount persistence for AH shares or holding companies.
- Suspension, delisting and corporate-action risk.

## Output Minimum

- Exact code, listing structure and timestamp.
- Latest reporting period.
- Business and financial-quality judgment.
- Governance and dilution review.
- Hong Kong peer and cross-listing valuation comparison.
- Southbound and liquidity analysis.
- Technical structure and key levels.
- Catalysts and invalidation conditions.
- GREEN / YELLOW / RED / DATA_BLOCKED.
- Source list and dates.

## Primary Source Baseline

Prefer:

1. HKEXnews company announcements and filings.
2. HKEX trading, settlement, Stock Connect and securities-list materials.
3. Securities and Futures Commission publications.
4. Hong Kong Government and Inland Revenue Department materials.
5. Company investor-relations materials and audited reports.
