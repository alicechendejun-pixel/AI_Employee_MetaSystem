"""
AutoHedge 调用工具
==================

调用 AutoHedge 的 Director / Quant / Risk / Execution 4 个 Agent，
拿到风控视角的仓位 + 风险建议。

路径: G:/我的云端硬盘/09-AI员工系统/03_Wealth_Trading_搞钱与交易/AutoHedge
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


AH_ROOT = Path(
    os.getenv(
        "AUTOHEDGE_ROOT",
        r"G:\我的云端硬盘\09-AI员工系统\03_Wealth_Trading_搞钱与交易\AutoHedge",
    )
)
AH_VENV_PY = AH_ROOT / "venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")


class AutoHedgeInput(BaseModel):
    ticker: str = Field(..., description="股票代码或加密资产 ticker")
    capital: float = Field(100000.0, description="组合资金（美元），用于仓位计算")
    risk_tolerance: str = Field("medium", description="low / medium / high")


class AutoHedgeRiskTool(BaseTool):
    name: str = "AutoHedge 风控 + 仓位"
    description: str = (
        "调用 AutoHedge 多 Agent 框架。Director 给策略 / Quant 做技术分析 / "
        "Risk 给仓位 / Execution 给具体下单建议。"
        "本系统主要用它产出的'风险警示 + 仓位百分比'部分，喂给内容里的'风险章节'。"
    )
    args_schema: Type[BaseModel] = AutoHedgeInput

    def _run(self, ticker: str, capital: float = 100000.0, risk_tolerance: str = "medium") -> str:
        if not AH_ROOT.exists():
            return json.dumps({
                "status": "skipped",
                "reason": f"AutoHedge 不在预期路径 {AH_ROOT}",
            }, ensure_ascii=False)

        py = AH_VENV_PY if AH_VENV_PY.exists() else sys.executable

        # AutoHedge 的入口
        example_script = AH_ROOT / "example.py"
        if not example_script.exists():
            return json.dumps({"status": "skipped", "reason": "example.py 不存在"}, ensure_ascii=False)

        # 用环境变量传参（AutoHedge 通常通过 env 读配置）
        env = os.environ.copy()
        env["AUTOHEDGE_TICKER"] = ticker
        env["AUTOHEDGE_CAPITAL"] = str(capital)
        env["AUTOHEDGE_RISK"] = risk_tolerance

        try:
            result = subprocess.run(
                [str(py), str(example_script)],
                cwd=str(AH_ROOT),
                capture_output=True,
                text=True,
                timeout=600,
                env=env,
                encoding="utf-8",
                errors="replace",
            )
        except subprocess.TimeoutExpired:
            return json.dumps({"status": "timeout", "ticker": ticker}, ensure_ascii=False)
        except FileNotFoundError as e:
            return json.dumps({"status": "skipped", "reason": str(e)}, ensure_ascii=False)

        # 查 logs 目录
        log_text = self._read_latest_log(AH_ROOT / "logs", ticker)

        return json.dumps({
            "status": "ok" if result.returncode == 0 else "partial",
            "ticker": ticker,
            "capital": capital,
            "risk_tolerance": risk_tolerance,
            "stdout_tail": result.stdout[-3000:] if result.stdout else "",
            "stderr_tail": result.stderr[-1000:] if result.stderr else "",
            "log_excerpt": log_text[:5000] if log_text else "",
            "extracted": self._extract_position(result.stdout, log_text),
        }, ensure_ascii=False)

    @staticmethod
    def _read_latest_log(log_dir: Path, ticker: str) -> str:
        if not log_dir.exists():
            return ""
        files = sorted(log_dir.glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
        for f in files[:5]:
            try:
                t = f.read_text(encoding="utf-8", errors="replace")
                if ticker.upper() in t.upper():
                    return t
            except Exception:
                continue
        return files[0].read_text(encoding="utf-8", errors="replace") if files else ""

    @staticmethod
    def _extract_position(stdout: str, log_text: str) -> dict:
        """从输出中抽出仓位建议 + 风险点"""
        import re
        text = (stdout or "") + "\n" + (log_text or "")
        out = {"position_pct": None, "stop_loss": None, "key_risks": []}
        m = re.search(r"position[^\d]{1,30}(\d{1,2}(?:\.\d+)?)\s*%", text, re.IGNORECASE)
        if m:
            out["position_pct"] = float(m.group(1))
        m = re.search(r"stop[\s_-]?loss[^\d]{1,30}(\$?\d{1,5}(?:\.\d+)?)", text, re.IGNORECASE)
        if m:
            out["stop_loss"] = m.group(1)
        for kw in ("liquidity", "regulatory", "earnings", "macro", "rate", "geopolitical"):
            if kw in text.lower():
                out["key_risks"].append(kw)
        return out
