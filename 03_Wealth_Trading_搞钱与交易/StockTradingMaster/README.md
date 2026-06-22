# Stock Trading Master System

统一的 A 股、美股、深度尽调、策略回测和风险控制 Skill 系统。

## 已集成模块

| 层级 | Skill | 用途 |
|---|---|---|
| A股市场适配 | `a-share-analysis` | 基本面、技术面、政策、资金流、A股交易规则 |
| A股筛选 | `a-share-screener` | 基本面与技术条件筛选 |
| A股数据 | `akshare` | A股、基金、期货等结构化数据接口 |
| 美股市场适配 | `us-stock-analysis` | 美股基本面、估值、技术面、同行比较 |
| 美股事件 | `earnings-calendar` | 财报日历 |
| 机构资金 | `institutional-flow-tracker` | 13F与机构持仓变化 |
| 期权分析 | `options-strategy-advisor` | Greeks与期权情景分析 |
| 问题标准化 | `stock-question-refiner` | 把自然语言问题转成尽调任务 |
| 深度尽调 | `stock-research-executor` | 八阶段机构式研究 |
| 回测 | `backtesting-trading-strategies` | 策略历史验证与绩效指标 |
| 风控否决 | `risk-manager` | 仓位、止损、集中度、对冲和风险预算 |
| 总控 | `stock-trading-master` | 路由、交叉验证、评分和红黄绿输出 |

## 安装

在本仓库根目录打开 PowerShell，执行：

```powershell
powershell -ExecutionPolicy Bypass -File ".\03_Wealth_Trading_搞钱与交易\StockTradingMaster\scripts\install_upstreams.ps1"
```

安装器只访问白名单中的五个公开 GitHub 仓库，并把选定 Skill 镜像到：

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
使用 stock-trading-master 比较 NVDA 和 AMD，持有期 6 到 12 个月，加入财务质量、估值、技术结构、机构持仓和风险预算。
```

```text
使用 stock-trading-master 回测：标普500成分股突破20日高点买入，2ATR止损，持有20日，计入手续费和滑点，必须做样本外测试。
```

## 系统决策流程

```text
用户问题
  ↓
问题标准化
  ↓
A股 / 美股市场适配
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
- 回测必须报告手续费、滑点、最大回撤和样本外结果。

## 关键文件

- 总控 Skill：`.claude/skills/stock-trading-master/SKILL.md`
- 上游注册表：`.claude/skills/stock-trading-master/config/upstreams.json`
- 统一报告格式：`.claude/skills/stock-trading-master/references/output-schema.md`
- 安装脚本：`scripts/install_upstreams.ps1`
- 来源与许可说明：`SOURCES.md`
