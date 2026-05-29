# FinMediaCrew — 金融自媒体变现 Agent 系统

> **一句话**：用 CrewAI 编排 FinRobot / TradingAgents / AutoHedge / AI-Trader 这 4 个交易 Agent 平台，把"交易分析"自动转成"金融自媒体内容工厂"，跑通研报 → 内容 → 分发 → 变现的闭环。

---

## 这是什么

**FinMediaCrew** = **金融分析栈** × **内容生产 Crew** × **变现漏斗**。

- 不是再造一个交易系统。
- 不是又一个 GPT 写文章。
- 是**把已有的 4 个交易 Agent 平台变成"内容产品的上游引擎"**——分析出来的结论 / 报告 / 信号 / 风控决策，被 CrewAI 接力加工成可发布的 4 种内容形态，进入分发 + 变现链路。

```
   ┌──────────────────────────────┐
   │  上游：4 个交易 AGENT SKILL  │
   │  (Wealth_Trading 文件夹)      │
   ├──────────────────────────────┤
   │  FinRobot      分析 / 研报     │
   │  TradingAgents 多 Agent 决策   │
   │  AutoHedge     风险 / 仓位     │
   │  AI-Trader     实盘 / 信号     │
   └─────────────┬────────────────┘
                 │ 结构化输出 (JSON / MD)
                 ▼
   ┌──────────────────────────────┐
   │   CrewAI 编排（本系统核心）   │
   ├──────────────────────────────┤
   │  DataAgent      数据采集       │
   │  AnalystAgent   交叉分析       │
   │  NarrativeAgent 反直觉叙事    │
   │  ContentAgent   多形态内容    │
   │  DistributionAgent 多平台分发 │
   │  MonetizationAgent 变现追踪   │
   └─────────────┬────────────────┘
                 ▼
   ┌──────────────────────────────┐
   │  下游：4 种内容产品           │
   │  公众号长文 / 小红书 / 视频脚本 │
   │  / 简报 / 付费内容            │
   └──────────────────────────────┘
```

---

## 为什么这样设计

**做"交易"本身赚钱有 3 个问题**：
1. 资金量小 → 杠杆赚不到大钱。
2. 一次性赚的 → 没有复利。
3. 心理压力大 → 长期不稳。

**做"金融自媒体"赚钱有 3 个好处**：
1. **资产化** —— 一篇好文章可以卖 5 年。
2. **复利** —— 粉丝累积 + 信任累积 + 内容库累积。
3. **杠杆** —— 同一份分析卖给 1000 个人 vs 自己交易。

但传统金融自媒体死在**内容生产成本**——
- 1 个分析师 = 1 周 1 篇深度文章。
- 不够频率 → 算法不推 → 没流量。

**FinMediaCrew 的核心命题**：

> 用 4 个交易 Agent 做"上游分析" + CrewAI 做"下游内容生产" = **1 个人 1 天 4-5 篇深度金融内容**。

实现**反规模化的金融个人 IP**——
- 1000 个深度铁粉。
- 每年 $100-500 订阅。
- $100K - $500K 年收入。
- 1 个人运营。

---

## 4 个交易 SKILL 的角色分工

| SKILL | 路径 | 在本系统的角色 |
|---|---|---|
| **FinRobot** | `09-AI员工系统/03_Wealth_Trading_搞钱与交易/FinRobot` | 主分析引擎：公司基本面 / 财报 / 多 Agent 研报生成 |
| **TradingAgents** | `.../TradingAgents` | 多角色辩论：基本面/情绪/技术/新闻 4 个分析师 + 研究员 + Trader + 风控的完整决策链 |
| **AutoHedge** | `.../AutoHedge` | 风控 + 仓位：Director/Quant/Risk/Execution 给出真实操作建议 |
| **AI-Trader** | `.../AI-Trader` | 跨平台信号同步 + 实盘验证（可选，TypeScript） |

**CrewAI** 不重新发明分析能力，**只做编排 + 内容化 + 分发**。

---

## 内容产品矩阵

### 1️⃣ 公众号长文（核心资产）
- 1500-3000 字深度文章。
- 1 周 2-3 篇。
- 价值锚：**4 个 SKILL 交叉分析 + 反直觉观点 + 真实案例**。
- 用户路径：免费阅读 → 关注 → 入星球。

### 2️⃣ 小红书图文（流量入口）
- 500 字 + 9 张图脚本。
- 1 天 1-2 篇。
- 价值锚：**金融认知卡片 / 投资术语图解**。
- 用户路径：刷到 → 关注 → 引流公众号。

### 3️⃣ YouTube/抖音视频脚本（深度认证）
- 8-12 分钟口播稿。
- 1 周 1 期。
- 价值锚：**深度选题 + 真实数据 + 私募风控视角**。
- 用户路径：看完 → 订阅 → 私聊 / 付费。

### 4️⃣ 每日简报（订阅产品）
- 200-500 字。
- 每天 1 篇。
- 价值锚：**前 1 小时市场关键事件 + 仓位建议**。
- 直接付费：**¥99/月 / ¥999/年**。

---

## 变现漏斗（5 阶段）

```
免费层 (吸粉)         付费层 (变现)         高客单层 (深度)
────────────────────  ──────────────────  ────────────────────
小红书 卡片            知识星球 ¥199/年      1 对 1 咨询 ¥2000/次
公众号 长文            付费简报 ¥99/月       Cohort 课程 ¥3000/期
免费简报 节选          会员视频 ¥49/月       Custom 研报 ¥5000/份
                      Gumroad 报告 ¥199    定制 Agent ¥10000/部署
```

**目标财务模型**（6-12 个月可达）：

| 阶段 | 月数 | 月收入 | 关键动作 |
|---|---|---|---|
| 0→1 | 1-3 | $0 - $500 | 跑通 Crew + 发 30 篇 + 攒 1000 粉 |
| 1→10 | 4-6 | $1K - $5K | 简报订阅 + 知识星球 + Gumroad 报告 |
| 10→100 | 7-12 | $10K - $30K | Cohort + 1对1 + Custom 部署 |

---

## 快速开始

```bash
# 1. 进入项目
cd "G:/我的云端硬盘/01-obsidian/04 AI知识库/09 金融记录共享/FinMediaCrew"

# 2. 创建 venv（避免污染上游 4 个 SKILL 的环境）
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # macOS/Linux

# 3. 安装依赖
pip install crewai crewai-tools langchain langchain-openai pyyaml python-dotenv yfinance requests

# 4. 配置 API Keys
cp crew/config/.env.example crew/config/.env
# 编辑 .env 填入：OPENAI_API_KEY / ANTHROPIC_API_KEY / FMP_API_KEY / 飞书 webhook

# 5. 跑一次完整 Crew
python crew/main.py --ticker NVDA --mode full

# 6. 只跑内容生产（用已有研报）
python crew/main.py --report-path report/nvda_2026.md --mode content_only
```

输出会到——

- `examples/output_<ticker>_<date>/` —— 4 种内容产品。
- 飞书 webhook —— 自动推送简报。
- 公众号草稿（可选 OAuth 授权后直接发布）。

---

## 项目结构

```
FinMediaCrew/
├── README.md                          ← 你在这里
├── ARCHITECTURE.md                    架构图 + Agent 分工 + 数据流
├── 启动指南.md                          ← 用户视角的 10 分钟启动
├── crew/                              CrewAI 核心代码
│   ├── main.py                        入口
│   ├── agents.py                      6 个 Agent 定义（Python）
│   ├── tasks.py                       任务流
│   ├── tools/                         上游 4 个 SKILL 的调用工具
│   │   ├── finrobot_tool.py
│   │   ├── tradingagents_tool.py
│   │   ├── autohedge_tool.py
│   │   └── market_data.py
│   └── config/
│       ├── agents.yaml                CrewAI 标准 yaml 配置
│       ├── tasks.yaml
│       └── .env.example
├── templates/                         4 种内容模板
│   ├── article_template.md
│   ├── xiaohongshu_template.md
│   ├── video_script_template.md
│   └── brief_template.md
├── monetization/                      变现设计
│   ├── product_design.md
│   ├── pricing.md
│   └── funnel.md
├── deployment/                        部署
│   ├── cron.md                        定时任务（每日/每周 schedule）
│   └── feishu_webhook.md              飞书集成
└── examples/                          真实案例
    └── output_nvda_2026-05/
```

---

## 接下来读哪个

- **想立刻跑通** → [`启动指南.md`](./启动指南.md)
- **想看架构** → [`ARCHITECTURE.md`](./ARCHITECTURE.md)
- **想看变现策略** → [`monetization/product_design.md`](./monetization/product_design.md)
- **想看代码** → [`crew/main.py`](./crew/main.py)

---

**作者**：德元君 / Alice Chen 私募风控视角 × AI Agent 编排 × 内容变现
**版本**：v0.1 · 2026-05-28
**License**：内部使用，不公开传播
