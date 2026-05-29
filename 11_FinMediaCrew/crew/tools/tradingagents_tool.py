"""
TradingAgents 调用工具
======================

调用多 Agent 辩论 pipeline：Fundamentals/Sentiment/News/Technical 4 个分析师 +
Research Manager + Trader + Risk。

路径: G:/我的云端硬盘/09-AI员工系统/03_Wealth_Trading_搞钱与交易/TradingAgents
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


TA_ROOT = Path(
    os.getenv(
        "TRADINGAGENTS_ROOT",
        r"G:\我的云端硬盘\09-AI员工系统\03_Wealth_Trading_搞钱与交易\TradingAgents",
    )
)
TA_VENV_PY = TA_ROOT / "venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")


class TradingAgentsInput(BaseModel):
    ticker: str = Field(..., description="股票代码")
    date: str = Field("", description="分析日期 YYYY-MM-DD，留空 = 今天")
    depth: str = Field("medium", description="shallow / medium / deep —— 影响 agent 辩论轮数")


class TradingAgentsDebateTool(BaseTool):
    name: str = "TradingAgents 多 Agent 辩论"
    description: str = (
        "调用 TradingAgents 多 Agent 框架，让 4 分析师 + 研究员 + Trader + 风控团队"
        "对一个 ticker 做完整辩论，输出 buy/hold/sell 决策 + 推理链。"
        "这是 4 个上游 SKILL 中最适合做'内容钩子'的工具，因为分歧点最丰富。"
    )
    args_schema: Type[BaseModel] = TradingAgentsInput

    def _run(self, ticker: str, date: str = "", depth: str = "medium") -> str:
        if not TA_ROOT.exists():
            return json.dumps({
                "status": "skipped",
                "reason": f"TradingAgents 不在预期路径 {TA_ROOT}",
            }, ensure_ascii=False)

        py = TA_VENV_PY if TA_VENV_PY.exists() else sys.executable

        # TradingAgents 有 CLI: cli/main.py
        cli_script = TA_ROOT / "cli" / "main.py"
        if not cli_script.exists():
            cli_script = TA_ROOT / "main.py"

        cmd = [str(py), str(cli_script), "--ticker", ticker]
        if date:
            cmd.extend(["--date", date])

        # 控制辩论深度的环境变量
        env = os.environ.copy()
        depth_map = {"shallow": "1", "medium": "2", "deep": "3"}
        env["TRADINGAGENTS_DEBATE_ROUNDS"] = depth_map.get(depth, "2")

        try:
            result = subprocess.run(
                cmd,
                cwd=str(TA_ROOT),
                capture_output=True,
                text=True,
                timeout=900,
                env=env,
                encoding="utf-8",
                errors="replace",
            )
        except subprocess.TimeoutExpired:
            return json.dumps({"status": "timeout", "ticker": ticker}, ensure_ascii=False)
        except FileNotFoundError as e:
            return json.dumps({"status": "skipped", "reason": str(e)}, ensure_ascii=False)

        # TradingAgents 一般把决策写到 logs/ 或 stdout
        return json.dumps({
            "status": "ok" if result.returncode == 0 else "partial",
            "ticker": ticker,
            "stdout_tail": result.stdout[-5000:] if result.stdout else "",
            "stderr_tail": result.stderr[-1000:] if result.stderr else "",
            "key_extract": self._extract_decision(result.stdout),
        }, ensure_ascii=False)

    @staticmethod
    def _extract_decision(stdout: str) -> dict:
        """从 stdout 里抽取关键决策"""
        out = {"action": None, "rationale": "", "target_price": None}
        if not stdout:
            return out
        lower = stdout.lower()
        for action in ("strong buy", "buy", "hold", "sell", "strong sell"):
            if action in lower:
                out["action"] = action.upper()
                break
        # 简单抽 target price
        import re
        m = re.search(r"target[^\d]{1,30}(\$?\d{1,5}(?:\.\d+)?)", stdout, re.IGNORECASE)
        if m:
            out["target_price"] = m.group(1)
        return out
