# 额度防封锁与系统级降维打击指南
**Quota Bypass & Rate Limit Strategies Manual**

这份指南解释了 `09_Quota_Bypass_Strategies_防封锁与额度优化` 文件夹下 4 个配置/脚本的运行逻辑。这是专为您量身定做的一套“第一性原理”组合拳，彻底告别盯着额度倒计时发呆的日子。

---

### 方案 1: Anything-LLM 自动截断流 (治标)
**脚本名称**: `1_anything_llm_rag_feeder.py`
**解决痛点**: 每次给 Claude 丢整个项目代码，导致 5 小时额度在 3 次对话内耗尽。
**第一性原理**: 废话不应该产生算力成本。
**使用方法**:
1. 启动您本地的 Anything-LLM 服务。
2. 在网页设置中生成一个 API Key，并在页面上创建一个叫 `ai-agents-knowledge` 的工作区。
3. 把 API Key 填入 `1_anything_llm_rag_feeder.py` 脚本的代码头部。
4. 运行脚本：它会自动把那 500 个项目的代码拆碎并向量化入库。
5. 之后让 Claude 连接 Anything-LLM 的对话接口即可。Token 消耗立减 95%。

---

### 方案 2: Dify 自动降级模型网关 (治本)
**配置文件**: `2_dify_model_router_workflow.yml`
**解决痛点**: 单一模型（如 Claude）达到限制时，系统直接宕机。
**第一性原理**: 算力是流动的，一条路堵死就自动走另一条路。
**使用方法**:
1. 启动您安装的 Dify 框架。
2. 点击右上角“导入工作流(Import Workflow)”，选择本目录下的 `2_dify_model_router_workflow.yml` 文件。
3. 导入后您会看到一个图形化界面：主干道连着 Claude 3.5 Sonnet，当这根线由于 `429 Too Many Requests` 或无响应断裂时，下方的红色回退线（Fallback）会自动接管，将请求无缝发给 Gemini 1.5 Flash。
4. 您以后所有的高并发任务，全部通过这个 Dify 路由接口对外暴露。

---

### 方案 3: CrewAI 高低端模型流水线 (系统级)
**脚本名称**: `3_crewai_high_low_tier_workers.py`
**解决痛点**: 拿最贵的大脑干粗活。
**第一性原理**: 只有最终决策需要顶级智慧，数据过滤只需要低级算力。
**使用方法**:
1. 确保安装了 `crewai` 依赖（就在 `04_Social_Network_社交与个人IP` 文件夹里）。
2. 在终端配置您的 API Key 环境变量：
   ```bash
   set GEMINI_API_KEY=您的Gemini_Key
   set ANTHROPIC_API_KEY=您的Claude_Key
   ```
3. 运行 `python 3_crewai_high_low_tier_workers.py`。
4. 剧本开始：Gemini 扮演“初级研究员”以极低成本通读数万字垃圾代码，提炼出 500 字。Claude 扮演“高级架构师”接手这 500 字，做第一性原理设计。省流极致打法。

---

### 方案 4: n8n 429 报错自动睡眠流 (自动化)
**配置文件**: `4_n8n_429_sleep_bypass.json`
**解决痛点**: 需要人盯着进度条，不能通宵挂机。
**第一性原理**: 用时间换空间，遇到封锁直接挂起，自动恢复。
**使用方法**:
1. 打开 n8n 的图形界面。
2. 点击右上角的“Import from File (从文件导入)”，选择 `4_n8n_429_sleep_bypass.json`。
3. 您会看到一条包含 `If 429 Error` 的分支。如果 Claude 接口报错，它会走向下方的 `Wait` 节点（默认设置 3.5 小时）。
4. 时间到了之后，它会自己醒来重新向 Claude 发起刚才失败的那个请求，完全不需要人工干预。

---

> **INTP 的进阶建议**：
> 最完美的终局是将以上四者结合：在 **n8n** 里面调度 **CrewAI** 脚本，而 CrewAI 背后请求的是 **Dify** 的负载均衡路由，Dify 的知识来源又是被 **Anything-LLM** 浓缩过的。
> 这样，您就打造了一台**永远不会被封禁、成本无限趋近于 0、且具备最顶级思考能力**的数据工厂。
