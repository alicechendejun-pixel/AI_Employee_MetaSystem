---
name: risk-manager
description: Apply a final risk veto to stock ideas and portfolios using position sizing, thesis invalidation, liquidity, gap risk, concentration, correlation and stress scenarios. Use after research or backtesting and before any paper-trading plan.
version: 1.0.0
---

# Risk Manager

## Authority

Risk review is the final gate. It may downgrade or reject an otherwise attractive idea.

This skill produces research and paper-trading controls only. It does not place orders or manage broker credentials.

## Required Inputs

Use supplied information only:

- Instrument and market.
- Entry concept and thesis.
- Invalidation condition.
- Intended holding period.
- Account size, current holdings and cost basis when available.
- Maximum acceptable loss when available.

Do not invent account size or risk tolerance.

## Risk Layers

### 1. Thesis risk

State what business, financial, policy, event or price behavior would prove the thesis wrong. Distinguish temporary volatility from thesis failure.

### 2. Position risk

When account information is available, calculate:

- Risk per share or unit.
- Maximum loss at the invalidation level.
- Position risk as a percentage of account equity.
- Position size consistent with the stated risk budget.

When account information is missing, provide formulas and scenario ranges rather than a false precise size.

### 3. Liquidity and execution risk

Review:

- Average traded value and volume.
- Bid-ask spread.
- Suspension or price-limit risk.
- Gap risk around earnings and announcements.
- Short borrow and options liquidity when relevant.
- Whether the proposed size can be exited realistically.

### 4. Portfolio concentration

Check:

- Single-name concentration.
- Sector and industry concentration.
- Country and currency exposure.
- Factor overlap such as high beta, duration, AI, commodities or small caps.
- Correlation with existing positions.
- Hidden concentration through ETFs or related companies.

### 5. Event risk

List dated events that can create discontinuous losses. Recommend reducing risk, waiting, hedging or accepting the event explicitly rather than treating it as ordinary volatility.

### 6. Stress scenarios

Estimate losses under at least:

- Ordinary adverse move.
- Severe market or sector move.
- Company-specific gap.
- Liquidity impairment.

State assumptions and avoid unsupported precision.

### 7. Stop and exit framework

Provide both when possible:

- Thesis-invalidation exit.
- Price or volatility reference.

Also define review triggers, time stop, profit-protection logic and conditions for adding rather than averaging down automatically.

## Veto Conditions

Return `RED` when any critical condition applies:

- No defensible invalidation condition.
- Expected loss exceeds the stated risk budget.
- Position cannot be exited with reasonable liquidity.
- Portfolio concentration becomes unacceptable.
- Event risk dominates expected return.
- Backtest is rejected or relies on material bias.
- Key data is missing or stale.

Return `YELLOW` for incomplete information, mixed evidence or manageable but meaningful risk. Return `GREEN` only when no critical veto remains.

## Output

- Risk status.
- Critical vetoes.
- Position-risk calculation or formula.
- Concentration findings.
- Liquidity and gap analysis.
- Event calendar.
- Ordinary and stress-loss scenarios.
- Invalidation and exit framework.
- Monitoring thresholds.
