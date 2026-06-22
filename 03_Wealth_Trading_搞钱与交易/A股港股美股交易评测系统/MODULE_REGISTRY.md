# A股港股美股交易评测系统模块登记表

## 内置核心模块

| 市场 / 层级 | Skill 路径 | 状态 | 职责 |
|---|---|---|---|
| 总控 | `.claude/skills/stock-trading-master/SKILL.md` | 已启用 | 市场路由、交叉验证、评分与红黄绿综合判断 |
| A股 | `.claude/skills/a-share-analysis/SKILL.md` | 已启用 | 内地市场规则、政策、资金流、基本面与技术面 |
| 港股 | `.claude/skills/hong-kong-stock-analysis/SKILL.md` | 已启用 | HKEX规则、T+2、港股通、手数/碎股、AH/ADR、治理和流动性 |
| 美股 | `.claude/skills/us-stock-analysis/SKILL.md` | 已启用 | SEC文件、财报预期、估值、持仓与技术面 |
| 问题标准化 | `.claude/skills/stock-question-refiner/SKILL.md` | 已启用 | 把自然语言问题转成研究任务书 |
| 深度研究 | `.claude/skills/stock-research-executor/SKILL.md` | 已启用 | 八阶段投资尽调 |
| 回测 | `.claude/skills/backtesting-trading-strategies/SKILL.md` | 已启用 | 偏差审计、交易成本建模、样本外验证 |
| 风控总闸 | `.claude/skills/risk-manager/SKILL.md` | 已启用 | 仓位、集中度、流动性、事件与压力风险否决 |

## 港股市场参考

- 规则基线：`.claude/skills/hong-kong-stock-analysis/references/market-rules.md`
- 主要信源：HKEX、HKEXnews、SFC、香港政府及税务局。
- 默认模式：研究、模拟和纸面交易。

## 调用示例

```text
stock-trading-master analyze 00700 腾讯控股 market=Hong-Kong horizon=6m
```

```text
stock-trading-master compare 09988 BABA cross-listing=true horizon=6-12m
```

```text
stock-trading-master backtest "20-day breakout with ATR stop" universe=HSI
```
