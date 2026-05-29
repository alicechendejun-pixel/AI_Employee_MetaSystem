# FinMediaCrew · 架构设计文档

## 1. 整体数据流

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 0：数据源                                                  │
│  ─────────────────                                               │
│  • FMP / Yahoo Finance / SEC EDGAR / Tushare / Web News          │
│  • 飞书 / Notion 历史研报                                          │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│  Layer 1：上游分析栈（已存在的 4 个 SKILL）                        │
│  ────────────────────────────                                    │
│  ┌─────────────┐  ┌─────────────────┐  ┌──────────┐  ┌────────┐ │
│  │  FinRobot   │  │ TradingAgents   │  │ AutoHedge│  │AI-Trader│ │
│  │  (研报)     │  │  (4 分析师辩论)  │  │ (风控/仓位)│  │(实盘)  │ │
│  └─────┬───────┘  └────────┬────────┘  └────┬─────┘  └───┬────┘ │
│        └───────────┬───────┴─────────────────┴─────────────┘    │
│                    │  结构化输出 (JSON + MD)                     │
└────────────────────┼────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│  Layer 2：CrewAI 编排层（本项目核心）                              │
│  ─────────────────────────────                                   │
│                                                                  │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────────┐      │
│  │ DataAgent   │───▶│ AnalystAgent │───▶│ NarrativeAgent │      │
│  │ 数据采集     │    │  交叉分析     │    │  反直觉叙事    │      │
│  └─────────────┘    └──────────────┘    └────────┬───────┘      │
│                                                  │              │
│  ┌──────────────────┐    ┌─────────────────┐    │              │
│  │ MonetizationAgent│◀───│ DistributionAgent│◀──┴─▶ ContentAgent│
│  │  变现追踪 / 漏斗 │    │  飞书/公众号/小红书│       4 种格式生产 │
│  └──────────────────┘    └─────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│  Layer 3：分发 + 变现                                             │
│  ─────────────────                                                │
│  飞书 webhook · 公众号 OAuth · 小红书 · YouTube                    │
│  Stripe · Gumroad · 知识星球 · 1对1 咨询                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. CrewAI Agent 详细分工

### 🧠 Agent 1 · DataAgent（数据采集）

**Role**: 资深金融数据工程师

**Goal**: 在 < 30 秒内为指定 ticker / topic 拿到 5 类数据。

**Tools**:
- `market_data.fetch_quote()` — 实时报价
- `market_data.fetch_financials()` — 财报
- `market_data.fetch_news()` — 新闻
- `market_data.fetch_sec_filings()` — SEC 文件
- `market_data.fetch_social_sentiment()` — Reddit/StockTwits

**Backstory**: 前彭博数据工程师 8 年，深度优化过亚太市场数据 pipeline。

**Output**: 标准 JSON，喂给 AnalystAgent。

---

### 📊 Agent 2 · AnalystAgent（交叉分析）

**Role**: 多视角金融分析总师

**Goal**: 调用 FinRobot + TradingAgents + AutoHedge 三路分析，输出**有共识 + 有分歧**的综合判断。

**Tools**:
- `finrobot_tool.run_equity_research()` — FinRobot 研报
- `tradingagents_tool.run_multi_agent_debate()` — TradingAgents 多 agent 辩论
- `autohedge_tool.get_risk_position()` — AutoHedge 仓位建议

**Backstory**: 前私募合伙人风控，擅长**找 4 个分析模型的"打架点"** —— 打架的地方才是文章的钩子。

**Output**:
```json
{
  "consensus": "三个模型都看多 NVDA 6 个月",
  "divergence": "TradingAgents 给目标价 $250，AutoHedge 仓位建议 8% / FinRobot 估值 $310",
  "hook_for_content": "为什么 TradingAgents 比 FinRobot 保守 24%？关键变量是数据中心 capex 假设",
  "raw_reports": {...}
}
```

---

### ✍️ Agent 3 · NarrativeAgent（反直觉叙事）

**Role**: 内容钩子总师 (前财经记者)

**Goal**: 把分析结果转成**有传播力的金融叙事**。

**核心规则**：
1. 找**反直觉点** —— 90% 的人误解的事。
2. 找**真实数据冲突** —— 数字打架最吸引人。
3. 找**人物 / 案例** —— 抽象数据要落到具体故事。
4. 不写垃圾鸡汤。

**Output**: 1 个核心 hook + 3 个支撑论点 + 1 个金句。

---

### 📝 Agent 4 · ContentAgent（多形态内容）

**Role**: 全栈金融内容生产者

**Goal**: 把同一个核心 hook 自动产出 4 种内容格式。

**Tools**:
- `templates/article_template.md` —— 公众号长文
- `templates/xiaohongshu_template.md` —— 小红书图文
- `templates/video_script_template.md` —— 视频口播
- `templates/brief_template.md` —— 每日简报

**重要约束**：
- 一份分析，4 种产品，避免**重复造轮子**。
- 但每种格式有**独家钩子**——不是简单复制粘贴。

**Output**: 4 个 markdown 文件 + 9 张配图脚本（小红书用）。

---

### 📡 Agent 5 · DistributionAgent（分发）

**Role**: 多平台分发工程师

**Goal**: 把 4 种内容**自动推送到对应平台**。

**Tools**:
- `feishu_webhook.send()` — 飞书群直接推。
- `wechat_official.create_draft()` — 公众号创建草稿（需 OAuth）。
- `xiaohongshu.post()` — 小红书发布（半自动，需人工审）。
- `youtube.upload()` — YouTube 上传（仅视频脚本，需要后续录制）。

**输出**: 发布日志 + URL 链接 + 草稿 ID。

---

### 💰 Agent 6 · MonetizationAgent（变现追踪）

**Role**: 增长 + 漏斗 + 定价分析师

**Goal**:
1. 追踪每篇内容**带来的关注 / 订阅 / 付费**。
2. 识别**爆款内容的共性**。
3. 决定**下周做什么选题**。
4. 提醒**推付费产品的最佳时机**。

**Tools**:
- `analytics.fetch_growth_metrics()` — 各平台数据。
- `funnel.compute_conversion()` — 计算 4 阶段漏斗。
- `recommender.suggest_next_topic()` — 推荐选题。

**Output**: 周报 + 月报 + 下周选题清单。

---

## 3. 任务流 (Task Pipeline)

CrewAI 用 **Sequential Process** 跑这个链，每个 task 输出喂给下一个：

```
Task 1: data_collection
  ↓ (raw_data.json)
Task 2: cross_analysis
  ↓ (cross_analysis.json)
Task 3: narrative_design
  ↓ (hook.md)
Task 4: content_production_4x
  ↓ (article.md, xiaohongshu.md, video.md, brief.md)
Task 5: distribution
  ↓ (distribution_log.json)
Task 6: monetization_tracking
  ↓ (monetization_report.md)
```

**关键**：每个 task 的 output 都写到 `examples/output_<ticker>_<date>/` 目录，**人可以中途接管 / 修改 / 重跑**。

---

## 4. 数据契约（Schema）

### 4.1 raw_data.json
```json
{
  "ticker": "NVDA",
  "as_of": "2026-05-28T14:00:00Z",
  "quote": {"price": 985, "change_pct": 2.1},
  "financials": {...},
  "news": [...],
  "sec_filings": [...],
  "sentiment": {"score": 0.65, "source_breakdown": {...}}
}
```

### 4.2 cross_analysis.json
```json
{
  "consensus": "string",
  "divergence_points": [
    {"model_a": "FinRobot", "model_b": "TradingAgents", "diff": "...", "magnitude": "high|mid|low"}
  ],
  "hook_for_content": "string",
  "risk_warnings": [...],
  "raw_reports": {
    "finrobot": "...",
    "tradingagents": "...",
    "autohedge": "..."
  }
}
```

### 4.3 hook.md
```
# {标题}
> 一句话钩子：{反直觉的核心观点}

## 3 个支撑论点
1. ...
2. ...
3. ...

## 金句收尾
> {1 句话}
```

### 4.4 4 种内容输出（见 `templates/`）

---

## 5. 跨平台兼容性

- **3 个 Python SKILL**（FinRobot / TradingAgents / AutoHedge）：通过 **subprocess + venv** 调用，**不污染本项目的 venv**。具体见 `crew/tools/*_tool.py`。
- **1 个 TS SKILL**（AI-Trader）：通过 **HTTP / `npx`** 调用，可选启用。
- **CrewAI 本身**：纯 Python，本项目独立 venv。

---

## 6. 失败模式 + 兜底

| 失败场景 | 处理 |
|---|---|
| FinRobot 调用超时 / 报错 | 跳过，AnalystAgent 仍用 TradingAgents + AutoHedge 输出 |
| 所有上游分析都失败 | 回退到**只用市场数据 + LLM** 生成基础分析 |
| 内容生产出 < 70 分 | 标记草稿状态，**不自动分发**，进人工审 |
| 分发平台 API 失败 | 写到本地 `examples/` 备份，飞书发"分发失败"告警 |
| LLM 额度耗尽 | 切换备用模型（OpenAI → Claude → 国产） |

---

## 7. 性能预期

| 阶段 | 时间 | Token 消耗 |
|---|---|---|
| 数据采集 | 20-40s | < 500 |
| 交叉分析 | 3-8 分钟 | 30K - 80K |
| 叙事设计 | 30-60s | 5K |
| 4 种内容生产 | 2-4 分钟 | 20K |
| 分发 | 10-30s | < 1K |
| **单次完整跑** | **8-15 分钟** | **60K-110K tokens** |

按 GPT-5.x 价格估算：**单次内容生产约 $0.5-1.5**。

按每天 2 个 ticker，每个产出 4 种内容 = **月成本 $30-90 + 月收入潜在 $3K-10K** = **80x+ ROI**。

---

## 8. 安全 + 合规

- ⚠️ 所有内容必须标注**"非投资建议"**。
- ⚠️ 不发布**未经多模型 cross-check** 的内容。
- ⚠️ 涉及个股的内容，必须有**风险警示** 章节。
- ⚠️ 不预测**短期价格** —— 只做框架性 / 结构性分析。

---

## 9. 后续路线图

| 版本 | 时间 | 新增 |
|---|---|---|
| v0.1 | 当前 | 基础 6 Agent + 4 内容格式 + 飞书分发 |
| v0.2 | 1 个月后 | 公众号 OAuth + 小红书半自动 + 数据持久化 (SQLite) |
| v0.3 | 3 个月后 | YouTube 自动剪辑 + AI 配音 + 视频自动发布 |
| v0.4 | 6 个月后 | 自动训练**专属 prompt** 让选题命中率上升 + Cohort 课程自动化 |
| v1.0 | 12 个月后 | 跨多 ticker / 多 topic 矩阵 + 用户画像驱动内容个性化 |

---

**下一步**：读 [`启动指南.md`](./启动指南.md) 或直接看 [`crew/main.py`](./crew/main.py)。
