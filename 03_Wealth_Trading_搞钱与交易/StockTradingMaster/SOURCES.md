# Upstream Sources and License Notes

The Stock Trading Master orchestration layer in this repository is original integration code. The installer downloads upstream projects into a local `vendor/` directory and mirrors selected skills for local agent discovery.

## Sources

### nicepkg/ai-workflow

- Repository: `https://github.com/nicepkg/ai-workflow`
- Skills: `a-share-analysis`, `a-share-screener`, `akshare`
- License observed: MIT
- Purpose: China A-share market analysis, screening and structured data access.

### tradermonty/claude-trading-skills

- Repository: `https://github.com/tradermonty/claude-trading-skills`
- Skills: `us-stock-analysis`, `earnings-calendar`, `institutional-flow-tracker`, `options-strategy-advisor`
- License observed: MIT
- Purpose: US equity, earnings, institutional-flow and options analysis.

### liangdabiao/Claude-Code-Stock-Deep-Research-Agent

- Repository: `https://github.com/liangdabiao/Claude-Code-Stock-Deep-Research-Agent`
- Skills: `stock-question-refiner`, `stock-research-executor`
- Top-level `LICENSE` file was not found during integration review.
- Purpose: structured question refinement and eight-phase stock due diligence.
- Redistribution note: the installer keeps this project as an external checkout. Review the upstream repository terms before redistributing its contents.

### jeremylongshore/claude-code-plugins-plus-skills

- Repository: `https://github.com/jeremylongshore/claude-code-plugins-plus-skills`
- Skill: `backtesting-trading-strategies`
- License observed: MIT
- Purpose: strategy backtesting and performance measurement.

### sickn33/antigravity-awesome-skills

- Repository: `https://github.com/sickn33/antigravity-awesome-skills`
- Skill: `risk-manager`
- License observed: MIT
- Purpose: position risk, portfolio concentration, stop and hedging controls.

## Update Policy

- Upstream code is not silently modified by the master orchestrator.
- Run the installer again to pull upstream updates.
- Review upstream changes before enabling them in production workflows.
- Live broker execution is outside this integration and remains disabled.
- Preserve all upstream copyright and license notices.
