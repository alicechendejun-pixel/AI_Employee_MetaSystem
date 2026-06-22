# Stock Trading Master Module Registry

## Native core modules

| Market / layer | Skill path | Status | Responsibility |
|---|---|---|---|
| Master orchestrator | `.claude/skills/stock-trading-master/SKILL.md` | Enabled | Market routing, cross-validation, scoring, red-yellow-green synthesis |
| A-share | `.claude/skills/a-share-analysis/SKILL.md` | Enabled | Mainland market rules, policy, capital flow, fundamentals and technicals |
| Hong Kong | `.claude/skills/hong-kong-stock-analysis/SKILL.md` | Enabled | HKEX rules, T+2, Stock Connect, board/odd lots, AH/ADR, governance and liquidity |
| US | `.claude/skills/us-stock-analysis/SKILL.md` | Enabled | SEC filings, earnings expectations, valuation, ownership and technicals |
| Question refinement | `.claude/skills/stock-question-refiner/SKILL.md` | Enabled | Convert natural-language questions into research briefs |
| Deep research | `.claude/skills/stock-research-executor/SKILL.md` | Enabled | Eight-phase investment due diligence |
| Backtesting | `.claude/skills/backtesting-trading-strategies/SKILL.md` | Enabled | Bias audit, transaction-cost modelling, sample-out validation |
| Risk governor | `.claude/skills/risk-manager/SKILL.md` | Enabled | Position, concentration, liquidity, event and stress-risk veto |

## Hong Kong market reference

- Rules baseline: `.claude/skills/hong-kong-stock-analysis/references/market-rules.md`
- Primary sources: HKEX, HKEXnews, SFC and Hong Kong Government / Inland Revenue Department.
- Default mode: research, simulation and paper trading only.

## Routing examples

```text
stock-trading-master analyze 00700 腾讯控股 market=Hong-Kong horizon=6m
```

```text
stock-trading-master compare 09988 BABA cross-listing=true horizon=6-12m
```

```text
stock-trading-master backtest "20-day breakout with ATR stop" universe=HSI
```
