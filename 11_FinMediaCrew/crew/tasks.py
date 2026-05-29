"""
CrewAI Task Pipeline 定义
=========================

6 个 Task 串成 Sequential Process。
每个 Task 的 output 喂给下一个。
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from crewai import Task, Agent


def _outpath(ctx: dict, name: str) -> str:
    return str(Path(ctx["output_dir"]) / name)


# ─────────────────────────────────────────────────────────────────
def task_data_collection(agent: Agent, ctx: dict) -> Task:
    target = ctx.get("ticker") or ctx.get("topic")
    return Task(
        name="data_collection",
        description=(
            f"为目标 {target} 采集 5 类数据：\n"
            f"1) 实时报价（涨跌幅、成交量、市值）\n"
            f"2) 最新季度财报（YoY、QoQ、关键指标）\n"
            f"3) 7 天内新闻头条（剔除噪音）\n"
            f"4) 最近 1 份 SEC filings 摘要（若有）\n"
            f"5) 社交情绪打分（Reddit + StockTwits）\n\n"
            f"输出严格 JSON，写到 {_outpath(ctx, 'raw_data.json')}。"
            f"截止时间戳：{ctx.get('as_of')}。"
        ),
        expected_output=(
            "符合 schema 的 JSON 字符串，包含 ticker、as_of、quote、financials、news、sec_filings、sentiment 字段。"
        ),
        agent=agent,
        output_file=_outpath(ctx, "raw_data.json"),
    )


# ─────────────────────────────────────────────────────────────────
def task_cross_analysis(agent: Agent, ctx: dict, deps: List[Task]) -> Task:
    target = ctx.get("ticker") or ctx.get("topic")
    return Task(
        name="cross_analysis",
        description=(
            f"基于上一步采集的数据，对 {target} 做 3 路交叉分析：\n"
            f"1) 调用 FinRobotEquityResearchTool —— 拿到 FinRobot 的研报式分析\n"
            f"2) 调用 TradingAgentsDebateTool —— 拿到 4 分析师 + 研究员 + Trader + 风控的辩论结论\n"
            f"3) 调用 AutoHedgeRiskTool —— 拿到 Director/Quant/Risk/Execution 的仓位建议\n\n"
            f"然后做 meta 分析：\n"
            f"- 三个模型的共识是什么？（一致看多/看空/中性？）\n"
            f"- 三个模型的分歧点 + 分歧的根本变量是什么？\n"
            f"- 哪个分歧点最适合做内容钩子？\n"
            f"- 风险警示有哪些？\n\n"
            f"输出 JSON 到 {_outpath(ctx, 'cross_analysis.json')}。"
        ),
        expected_output=(
            "JSON 含 consensus、divergence_points (list)、hook_for_content、risk_warnings (list)、raw_reports (dict) 字段。"
        ),
        agent=agent,
        context=deps,
        output_file=_outpath(ctx, "cross_analysis.json"),
    )


# ─────────────────────────────────────────────────────────────────
def task_narrative_design(agent: Agent, ctx: dict, deps: List[Task]) -> Task:
    return Task(
        name="narrative_design",
        description=(
            "基于上一步的 cross_analysis，写一个有传播力的金融叙事。"
            "格式：\n\n"
            "# {点击力标题}\n\n"
            "> 一句话钩子：{反直觉的核心观点}\n\n"
            "## 3 个支撑论点\n"
            "1. {论点 + 真实数据}\n"
            "2. {论点 + 真实数据}\n"
            "3. {论点 + 真实数据}\n\n"
            "## 关键人物 / 案例\n"
            "{1 个真实人物或公司案例，作为故事钩子}\n\n"
            "## 风险警示\n"
            "{1-3 条}\n\n"
            "## 金句收尾\n"
            "> {1 句话}\n\n"
            "**禁止**：鸡汤 / 排比 / 感叹号堆叠 / 廉价情绪。\n"
            "**必须**：反直觉 + 真实数据 + 短句多换行。\n\n"
            f"输出到 {_outpath(ctx, 'hook.md')}。"
        ),
        expected_output="符合上述格式的 markdown 内容。",
        agent=agent,
        context=deps,
        output_file=_outpath(ctx, "hook.md"),
    )


# ─────────────────────────────────────────────────────────────────
def task_content_production(agent: Agent, ctx: dict, deps: List[Task]) -> Task:
    return Task(
        name="content_production",
        description=(
            "基于上一步的 hook.md，自动产出 4 种内容格式，每种独立有钩子：\n\n"
            f"1) **公众号长文** → {_outpath(ctx, 'article.md')}\n"
            "   - 1500-3000 字\n"
            "   - 模板见 templates/article_template.md\n"
            "   - 结构：钩子 → 现象 → 深挖 → 框架 → 行动 → 金句\n\n"
            f"2) **小红书图文** → {_outpath(ctx, 'xiaohongshu.md')}\n"
            "   - 主文 500 字 + 9 张配图脚本（每张图标题 + 内容描述）\n"
            "   - 模板见 templates/xiaohongshu_template.md\n"
            "   - 必须有 5-8 个 hashtag\n\n"
            f"3) **视频口播脚本** → {_outpath(ctx, 'video_script.md')}\n"
            "   - 8-12 分钟时长（约 2500-3500 字）\n"
            "   - 模板见 templates/video_script_template.md\n"
            "   - 结构：钩子 30s / 铺垫 60s / 深挖 / 框架 / 收束 / 金句\n\n"
            f"4) **每日简报** → {_outpath(ctx, 'brief.md')}\n"
            "   - 200-500 字\n"
            "   - 模板见 templates/brief_template.md\n"
            "   - 适合飞书 / 微信群 / Twitter\n\n"
            "**铁律**：4 份内容必须**入口钩子不同**，但**核心观点一致**。"
        ),
        expected_output="4 个 markdown 文件全部写到 output_dir。返回简短总结。",
        agent=agent,
        context=deps,
    )


# ─────────────────────────────────────────────────────────────────
def task_distribution(agent: Agent, ctx: dict, deps: List[Task]) -> Task:
    dry_run = ctx.get("dry_run", False)
    return Task(
        name="distribution",
        description=(
            f"把 4 种内容分发到对应平台。dry_run={dry_run}。\n\n"
            "动作清单：\n"
            f"1) 简报 → 飞书群 webhook（{_outpath(ctx, 'brief.md')}）\n"
            f"2) 公众号长文 → 创建公众号草稿（{_outpath(ctx, 'article.md')}）\n"
            f"3) 小红书 → 输出到本地 + 提示人工发布（{_outpath(ctx, 'xiaohongshu.md')}）\n"
            f"4) 视频脚本 → 本地保存，提醒后续录制（{_outpath(ctx, 'video_script.md')}）\n\n"
            "如果是 dry_run，**只生成发布单不真发**。\n"
            f"输出日志到 {_outpath(ctx, 'distribution_log.json')}。"
        ),
        expected_output="distribution_log.json 含每个平台的 status + url / draft_id / error。",
        agent=agent,
        context=deps,
        output_file=_outpath(ctx, "distribution_log.json"),
    )


# ─────────────────────────────────────────────────────────────────
def task_monetization_tracking(agent: Agent, ctx: dict, deps: List[Task]) -> Task:
    return Task(
        name="monetization_tracking",
        description=(
            "本次内容生产完成，记录到变现追踪表：\n"
            "1) 内容主题 + 4 种产物的路径\n"
            "2) 预期 CTR / 留存率 / 订阅转化率\n"
            "3) 推荐何时推付费产品（基于近 30 天用户行为）\n"
            "4) 下周选题建议（基于本周表现）\n\n"
            f"输出到 {_outpath(ctx, 'monetization_report.md')}。"
        ),
        expected_output="markdown 报告 + 下周 3-5 个选题建议。",
        agent=agent,
        context=deps,
        output_file=_outpath(ctx, "monetization_report.md"),
    )


# ─────────────────────────────────────────────────────────────────
def build_pipeline(agents: Dict, ctx: dict) -> List[Task]:
    """构造 6 个 task 的完整 pipeline"""
    t1 = task_data_collection(agents["data_agent"], ctx)
    t2 = task_cross_analysis(agents["analyst_agent"], ctx, deps=[t1])
    t3 = task_narrative_design(agents["narrative_agent"], ctx, deps=[t2])
    t4 = task_content_production(agents["content_agent"], ctx, deps=[t3])
    t5 = task_distribution(agents["distribution_agent"], ctx, deps=[t4])
    t6 = task_monetization_tracking(agents["monetization_agent"], ctx, deps=[t1, t2, t3, t4, t5])
    return [t1, t2, t3, t4, t5, t6]
