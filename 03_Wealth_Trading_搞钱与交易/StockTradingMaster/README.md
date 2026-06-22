# Stock Trading Master System

统一的 A 股、港股、美股、深度尽调、策略回测和风险控制 Skill 系统。

## 已内置核心模块

| 层级 | Skill | 用途 |
|---|---|---|
| A股市场适配 | `a-share-analysis` | 基本面、技术面、政策、资金流、A股交易规则 |
| 港股市场适配 | `hong-kong-stock-analysis` | HKEX规则、港股通、AH/ADR比较、南向资金、治理、流动性和估值 |
| 美股市场适配 | `us-stock-analysis` | 美股基本面、估值、技术面、财报和机构定位 |
| 问题标准化 | `stock-question-refiner` | 把自然语言问题转成可执行尽调任务 |
| 深度尽调 | `stock-research-executor` | 八阶段机构式研究 |
| 回测 | `backtesting-trading-strategies` | 策略历史验证、偏差审计和样本外测试 |
| 风控否决 | `risk-manager` | 仓位、止损、集中度、流动性和压力测试 |
| 总控 | `stock-trading-master` | 路由、交叉验证、评分和红黄绿输出 |

这些核心 Skill 已经直接保存在 `.claude/skills/`，克隆仓库后即可使用，不需要额外安装。

## 港股模块覆盖

- 主板、GEM、H股、红筹、民营中资股和本地香港公司。
- 二次上市、双重主要上市、ADR及AH股价差比较。
- T+2结算、手数与碎股、收市竞价、VCM及港股交易成本。
- 港股通资格、南向资金、交易日历和跨境交易限制。
- 控股股东、关联交易、配股、供股、合股、回购和私有化。
- 港币、人民币双柜台、利率敏感性、低流动性和停牌风险。

## 可选上游增强

仓库同时保留白名单安装器，用于同步第三方增强模块，例如 A股筛选、AkShare、财报日历、13F机构资金和期权分析。

在本仓库根目录打开 PowerShell，执行：

```powershell
powershell -ExecutionPolicy Bypass -File ".\03_Wealth_Trading_搞钱与交易\StockTradingMaster\scripts\install_upstreams.ps1"
```

第三方 Skill 镜像到：

```text
.claude/skills/vendor/
```

上游仓库保存在：

```text
03_Wealth_Trading_搞钱与交易/StockTradingMaster/vendor/
```

## 使用

Claude Code 在仓库根目录启动后，可直接提出：

```text
使用 stock-trading-master 分析 688010 福光股份，中期视角，输出红黄绿灯、核心逻辑、反方逻辑、关键价位和失效条件。
```

```text
使用 stock-trading-master 分析港股 00700 腾讯控股，持有期6个月，加入南向资金、治理、估值、技术结构、催化剂和风险预算。
```

```text
使用 stock-trading-master 比较港股 09988 阿里巴巴和美股 BABA，调整汇率、ADR换算比例、流动性、交易成本和可转换限制，判断哪边风险收益比更高。
```

```text
使用 stock-trading-master 比较 NVDA 和 AMD，持有期 6 到 12 个月，加入财务质量、估值、技术结构、机构持仓和风险预算。
```

```text
使用 stock-trading-master 回测：恒生指数成分股突破20日高点买入，2ATR止损，持有20日，计入港股印花税、交易征费、滑点和碎股限制，必须做样本外测试。
```

## 系统决策流程

```text
用户问题
  ↓
问题标准化
  ↓
A股 / 港股 / 美股市场适配
  ↓
基本面、技术面、事件、反方研究并行
  ↓
八阶段深度尽调
  ↓
策略回测与稳健性检验
  ↓
风险管理否决层
  ↓
GREEN / YELLOW / RED / DATA_BLOCKED
```

## 重要边界

- 默认仅研究、模拟和纸面交易。
- 不读取或写入券商密钥。
- 不自动实盘下单。
- 风控模块拥有最终否决权。
- 数据过期、信源冲突或关键资料缺失时必须降级为黄灯或 `DATA_BLOCKED`。
- 回测必须报告手续费、税费、滑点、最大回撤和样本外结果。
- AH股或ADR价差不能直接视为无风险套利，必须考虑汇率、换算比例、流动性和不可自由转换限制。

## 关键文件

- 总控：`.claude/skills/stock-trading-master/SKILL.md`
- A股：`.claude/skills/a-share-analysis/SKILL.md`
- 港股：`.claude/skills/hong-kong-stock-analysis/SKILL.md`
- 美股：`.claude/skills/us-stock-analysis/SKILL.md`
- 问题标准化：`.claude/skills/stock-question-refiner/SKILL.md`
- 深度尽调：`.claude/skills/stock-research-executor/SKILL.md`
- 回测：`.claude/skills/backtesting-trading-strategies/SKILL.md`
- 风控：`.claude/skills/risk-manager/SKILL.md`
- 上游注册表：`.claude/skills/stock-trading-master/config/upstreams.json`
- 统一报告格式：`.claude/skills/stock-trading-master/references/output-schema.md`
- 可选增强安装器：`scripts/install_upstreams.ps1`
- 来源与许可：`SOURCES.md`
