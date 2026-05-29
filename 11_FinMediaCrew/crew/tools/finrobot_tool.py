"""
FinRobot 调用工具
=================

通过 subprocess 调用 FinRobot 的研报生成 pipeline，不污染本项目 venv。

FinRobot 路径: G:/我的云端硬盘/09-AI员工系统/03_Wealth_Trading_搞钱与交易/FinRobot
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


FINROBOT_ROOT = Path(
    os.getenv(
        "FINROBOT_ROOT",
        r"G:\我的云端硬盘\09-AI员工系统\03_Wealth_Trading_搞钱与交易\FinRobot",
    )
)
FINROBOT_VENV_PY = FINROBOT_ROOT / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")


class FinRobotInput(BaseModel):
    ticker: str = Field(..., description="股票代码，如 NVDA / AAPL / 0700.HK")
    company_name: str = Field("", description="公司全名，可选；FinRobot 用它生成研报标题")
    horizon: str = Field("1Y", description="分析时间维度，如 1Y / 6M / 3M")


class FinRobotEquityResearchTool(BaseTool):
    name: str = "FinRobot 研报生成"
    description: str = (
        "调用 FinRobot 的多 Agent equity research pipeline，生成机构级研报。"
        "输入 ticker，输出 markdown / JSON 形式的深度研报，包含基本面 / 估值 / 风险。"
    )
    args_schema: Type[BaseModel] = FinRobotInput

    def _run(self, ticker: str, company_name: str = "", horizon: str = "1Y") -> str:
        if not FINROBOT_ROOT.exists():
            return json.dumps({
                "status": "skipped",
                "reason": f"FinRobot 不在预期路径 {FINROBOT_ROOT}",
                "fallback": "AnalystAgent 将只用其他模型",
            }, ensure_ascii=False)

        script = FINROBOT_ROOT / "finrobot_equity" / "core" / "src" / "generate_financial_analysis.py"
        if not script.exists():
            # 退到 demo 入口
            script = FINROBOT_ROOT / "agent_builder_demo.py"

        py = FINROBOT_VENV_PY if FINROBOT_VENV_PY.exists() else sys.executable

        cmd = [
            str(py),
            str(script),
            "--company-ticker", ticker,
            "--company-name", company_name or ticker,
        ]

        try:
            result = subprocess.run(
                cmd,
                cwd=str(FINROBOT_ROOT),
                capture_output=True,
                text=True,
                timeout=600,
                encoding="utf-8",
                errors="replace",
            )
        except subprocess.TimeoutExpired:
            return json.dumps({"status": "timeout", "ticker": ticker}, ensure_ascii=False)
        except FileNotFoundError as e:
            return json.dumps({"status": "skipped", "reason": str(e)}, ensure_ascii=False)

        # FinRobot 通常把研报写到 report/ 目录
        report_dir = FINROBOT_ROOT / "report"
        latest = self._find_latest_report(report_dir, ticker) if report_dir.exists() else None
        report_text = latest.read_text(encoding="utf-8", errors="replace") if latest else ""

        return json.dumps({
            "status": "ok" if result.returncode == 0 else "partial",
            "ticker": ticker,
            "stdout_tail": result.stdout[-2000:] if result.stdout else "",
            "stderr_tail": result.stderr[-1000:] if result.stderr else "",
            "report_path": str(latest) if latest else None,
            "report_text": report_text[:30000],   # 截断防爆 LLM 上下文
        }, ensure_ascii=False)

    @staticmethod
    def _find_latest_report(report_dir: Path, ticker: str) -> Path | None:
        candidates = sorted(
            [p for p in report_dir.glob(f"*{ticker}*") if p.is_file()],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        return candidates[0] if candidates else None
