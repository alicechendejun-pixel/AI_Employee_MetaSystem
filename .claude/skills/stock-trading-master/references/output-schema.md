# Stock Trading Master Output Schema

Use this structure for every final decision package. Omit sections only when they are genuinely irrelevant, and state why.

## 1. Decision Header

- Market:
- Ticker / company:
- Analysis timestamp and timezone:
- Market session status:
- Horizon:
- User objective:
- Final status: GREEN / YELLOW / RED / DATA_BLOCKED
- Confidence: High / Medium / Low

## 2. Executive Judgment

Provide no more than five sentences:

- Primary thesis.
- Strongest confirming evidence.
- Strongest counter-thesis.
- Main invalidation condition.
- Risk-adjusted conclusion.

## 3. Scorecard

| Dimension | Score 0-5 | Weight | Weighted score | Evidence |
|---|---:|---:|---:|---|
| Business quality | | | | |
| Financial quality | | | | |
| Valuation | | | | |
| Industry / catalysts | | | | |
| Technical structure | | | | |
| Evidence quality | | | | |
| Strategy robustness | | | | |
| Risk-adjusted attractiveness | | | | |

List any critical veto below the table. A veto overrides the weighted total.

## 4. Evidence Map

Separate facts from interpretation.

| Claim | Type: Fact / Inference / Scenario | Source | Date | Confidence |
|---|---|---|---|---|

## 5. Fundamental and Valuation View

- Revenue, profit and free-cash-flow trend.
- Balance-sheet strength.
- Earnings quality and accounting anomalies.
- Competitive position and moat.
- Historical and peer-relative valuation.
- Scenario valuation range and assumptions.

## 6. Technical and Market Structure

- Primary trend by relevant timeframe.
- Volume and breadth confirmation.
- Support, resistance and invalidation levels.
- RSI, MACD, moving averages or other indicators only when data is current.
- Gap, liquidity and event-risk observations.

## 7. Catalysts and Calendar

| Date / window | Event | Bullish implication | Bearish implication | What to verify |
|---|---|---|---|---|

## 8. Backtest Report

When a rule-based strategy is involved, include:

- Universe and period.
- Exact entry and exit rules.
- Benchmark.
- Trade count.
- Win rate.
- Payoff ratio.
- Expectancy.
- Annualized return or CAGR.
- Maximum drawdown.
- Sharpe or alternative risk metric.
- Fees and slippage assumptions.
- In-sample versus out-of-sample results.
- Bias and data-quality warnings.

Conclude with PASS / CONDITIONAL / REJECTED.

## 9. Risk Governor

- Maximum thesis risk per position.
- Suggested position-size range only when the user's account constraints are known.
- Portfolio concentration and factor overlap.
- Ordinary-loss scenario.
- Stress-loss scenario.
- Thesis invalidation.
- Price or volatility stop reference.
- Event-risk treatment.
- Hedging need, if any.

## 10. Action Matrix

Do not issue unconditional commands. Express conditional plans.

| Condition | Status | Research action | Paper-trading action | Reassessment trigger |
|---|---|---|---|---|
| Bull case confirmed | | | | |
| Mixed evidence | | | | |
| Thesis invalidated | | | | |

## 11. Monitoring Checklist

List the five to ten data points that can strengthen or break the thesis. Include threshold, source and review cadence.

## 12. Sources and Module Trace

List:

- Primary sources.
- Secondary sources.
- Upstream skills used.
- Upstream skills unavailable.
- Data gaps and unresolved contradictions.
