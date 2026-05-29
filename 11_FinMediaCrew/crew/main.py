"""
FinMediaCrew — 金融自媒体变现 Agent 入口
======================================

用 CrewAI 编排 6 个 Agent，把 FinRobot/TradingAgents/AutoHedge 的分析
转成可发布的金融自媒体内容。

Usage:
    python crew/main.py --ticker NVDA
    python crew/main.py --ticker NVDA --mode content_only --report-path ../report/nvda.md
    python crew/main.py --topic "美联储 6 月降息" --mode topic
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# ── 路径 ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "crew"))

# CrewAI
from crewai import Crew, Process

from agents import build_all_agents
from tasks import build_pipeline


# ─────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="FinMediaCrew 金融自媒体 Agent")
    p.add_argument("--ticker", type=str, default=None, help="股票代码，如 NVDA / 0700.HK")
    p.add_argument("--topic", type=str, default=None, help="宏观话题，如 '美联储降息'")
    p.add_argument(
        "--mode",
        choices=["full", "content_only", "topic", "brief_only"],
        default="full",
        help="full=完整 6 Agent / content_only=用已有研报生产内容 / topic=纯宏观主题 / brief_only=只生成简报",
    )
    p.add_argument("--report-path", type=str, default=None, help="content_only 模式下的已有研报路径")
    p.add_argument("--output-dir", type=str, default=None, help="输出目录，默认 examples/output_<ticker>_<date>/")
    p.add_argument("--dry-run", action="store_true", help="只生成内容，不分发")
    return p.parse_args()


# ─────────────────────────────────────────────────────────────────
def setup_output_dir(args: argparse.Namespace) -> Path:
    """准备输出目录"""
    if args.output_dir:
        outdir = Path(args.output_dir)
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
        slug = args.ticker or args.topic.replace(" ", "_")[:20] if args.topic else "general"
        outdir = PROJECT_ROOT / "examples" / f"output_{slug}_{date_str}"
    outdir.mkdir(parents=True, exist_ok=True)
    print(f"📂 Output: {outdir}")
    return outdir


# ─────────────────────────────────────────────────────────────────
def build_initial_context(args: argparse.Namespace, outdir: Path) -> dict:
    """构造初始上下文，喂给第一个 task"""
    ctx = {
        "ticker": args.ticker,
        "topic": args.topic,
        "as_of": datetime.now().isoformat(),
        "output_dir": str(outdir),
        "mode": args.mode,
        "dry_run": args.dry_run,
    }
    if args.report_path and Path(args.report_path).exists():
        ctx["existing_report"] = Path(args.report_path).read_text(encoding="utf-8")
        print(f"📄 Loaded existing report: {args.report_path}")
    return ctx


# ─────────────────────────────────────────────────────────────────
def main() -> int:
    args = parse_args()
    load_dotenv(PROJECT_ROOT / "crew" / "config" / ".env")

    if not args.ticker and not args.topic:
        print("❌ 必须提供 --ticker 或 --topic")
        return 1

    print("=" * 60)
    print(f"🚀 FinMediaCrew · Mode={args.mode}")
    print(f"   Target: {args.ticker or args.topic}")
    print("=" * 60)

    outdir = setup_output_dir(args)
    initial_ctx = build_initial_context(args, outdir)

    # 写入 context 供 Agent 读取
    (outdir / "_context.json").write_text(
        json.dumps(initial_ctx, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 构建 6 个 Agent + Task pipeline
    agents = build_all_agents(initial_ctx)
    tasks = build_pipeline(agents, initial_ctx)

    # 根据 mode 截断 pipeline
    if args.mode == "content_only":
        tasks = [t for t in tasks if t.name in ("narrative_design", "content_production", "distribution")]
    elif args.mode == "brief_only":
        tasks = [t for t in tasks if t.name in ("data_collection", "narrative_design", "content_production")]

    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    try:
        result = crew.kickoff(inputs=initial_ctx)
    except KeyboardInterrupt:
        print("\n⏹️  用户中断")
        return 130
    except Exception as e:
        print(f"\n❌ Crew 执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # 写入最终结果
    (outdir / "_result.json").write_text(
        json.dumps({"status": "ok", "result_summary": str(result)[:5000]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("\n" + "=" * 60)
    print(f"✅ 完成 · 产物在: {outdir}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
