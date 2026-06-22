# 上游来源与许可说明

本仓库中的 A股港股美股交易评测系统总控层为原创集成代码。可选安装器会把第三方项目下载到本地 `vendor/` 目录，并把选定 Skill 镜像到本地 Agent 可发现路径。

## 来源

### nicepkg/ai-workflow

- 仓库：`https://github.com/nicepkg/ai-workflow`
- Skills：`a-share-analysis`、`a-share-screener`、`akshare`
- 已观察到的许可：MIT
- 用途：A股市场分析、筛选与结构化数据访问。

### tradermonty/claude-trading-skills

- 仓库：`https://github.com/tradermonty/claude-trading-skills`
- Skills：`us-stock-analysis`、`earnings-calendar`、`institutional-flow-tracker`、`options-strategy-advisor`
- 已观察到的许可：MIT
- 用途：美股、财报、机构资金与期权分析。

### liangdabiao/Claude-Code-Stock-Deep-Research-Agent

- 仓库：`https://github.com/liangdabiao/Claude-Code-Stock-Deep-Research-Agent`
- Skills：`stock-question-refiner`、`stock-research-executor`
- 集成检查时未发现顶层 `LICENSE` 文件。
- 用途：问题标准化与八阶段股票深度尽调。
- 再分发说明：安装器把该项目保留为外部检出；再分发其内容前应检查上游仓库条款。

### jeremylongshore/claude-code-plugins-plus-skills

- 仓库：`https://github.com/jeremylongshore/claude-code-plugins-plus-skills`
- Skill：`backtesting-trading-strategies`
- 已观察到的许可：MIT
- 用途：策略回测与绩效衡量。

### sickn33/antigravity-awesome-skills

- 仓库：`https://github.com/sickn33/antigravity-awesome-skills`
- Skill：`risk-manager`
- 已观察到的许可：MIT
- 用途：仓位风险、组合集中度、止损与对冲控制。

## 更新政策

- 总控不会静默修改上游代码。
- 重新运行安装器可拉取上游更新。
- 在生产工作流启用前应审查上游变化。
- 实盘券商执行不属于本集成范围，并保持关闭。
- 必须保留全部上游版权与许可说明。
