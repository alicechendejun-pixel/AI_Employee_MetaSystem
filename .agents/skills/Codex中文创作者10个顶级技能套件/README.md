# Codex 中文创作者 10 个顶级技能套件

这是一整套集中管理的中文内容生产线，所有 Skill 都放在同一个中文总目录：

```text
.agents/skills/Codex中文创作者10个顶级技能套件/
```

## 中文目录结构

```text
Codex中文创作者10个顶级技能套件/
├── 01_中文去AI味与文风清洗/
├── 02_选题Hook与内容诊断编辑器/
├── 03_调研与长文写作一体化/
├── 04_NotebookLM知识库写作助手/
├── 05_AI热点与深度研究工作台/
├── 06_Punk中文封面生成器/
├── 07_鬼藏社交卡片与公众号封面/
├── 08_宝玉信息图与结构图生成器/
├── 09_Ian小黑正文手绘配图/
├── 10_HTML发布与成品排版/
├── README.md
└── 安全边界说明.md
```

> 每个子目录中的 `SKILL.md` 是 Codex 强制识别文件名，不能改成中文；但总目录、子目录、页面标题和用途说明均为中文。

## 10 个 Skill

| 顺序 | 中文标题 | Codex 调用名 | 上游仓库 | 核心用途 |
|---|---|---|---|---|
| 01 | 中文去 AI 味与文风清洗 | `creator-stop-slop` | `hardikpandya/stop-slop` | 删除模板句、空洞转折、机械节奏和假深刻表达 |
| 02 | 选题、Hook 与内容诊断编辑器 | `creator-dbskill-editor` | `dontbesilent2025/dbskill` | 判断选题是否成立，诊断标题、开头、传播张力和平台形式 |
| 03 | 调研与长文写作一体化 | `creator-research-writer` | `ComposioHQ/awesome-claude-skills/content-research-writer` | 调研、提纲、引用、写作、逐段反馈和终稿检查 |
| 04 | NotebookLM 知识库写作助手 | `creator-notebooklm` | `PleasePrompto/notebooklm-skill` | 基于用户资料库检索和写作，减少事实幻觉 |
| 05 | AI 热点与深度研究工作台 | `creator-aihot-research` | `KKKKhazix/khazix-skills/aihot` | 获取最新 AI 动态、模型发布、产品、论文和行业事件 |
| 06 | Punk 中文封面生成器 | `creator-punk-cover` | `adrianpunk/Punk-Skill/skills/punk-cover` | 为小红书、公众号、X 和文章生成中文封面方案与图片 |
| 07 | 鬼藏社交卡片与公众号封面 | `creator-guizang-cards` | `op7418/guizang-social-card-skill` | 长文拆卡、小红书组图、公众号 21:9 + 1:1 封面对 |
| 08 | 宝玉信息图与结构图生成器 | `creator-baoyu-infographic` | `JimLiu/baoyu-skills/skills/baoyu-infographic` | 将流程、对比、框架、清单和方法论转换为信息图 |
| 09 | Ian 小黑正文手绘配图 | `creator-xiaohei-illustrations` | `helloianneo/ian-xiaohei-illustrations` | 为中文长文生成有记忆点的 16:9 手绘正文配图 |
| 10 | HTML 发布与成品排版 | `creator-html-publisher` | `nexu-io/html-anything` | 将 Markdown、文章和数据转换成可发布的单文件 HTML |

## 推荐生产线

```text
02 选题、Hook 与内容诊断
  → 05 最新热点与外部材料 / 04 私有知识库材料
  → 03 调研、提纲与正文
  → 01 去 AI 味与文风清洗
  → 06 封面 / 07 社交卡片 / 08 信息图 / 09 正文配图
  → 10 HTML 成品发布
```

## 最小高频组合

1. `creator-dbskill-editor`：判断内容值不值得做。
2. `creator-stop-slop`：清除 AI 写作痕迹。
3. `creator-punk-cover`：解决第一眼点击。

## 集成规则

- 每个中文子目录都是一个独立、可发现的 Codex Skill。
- 中文标题、触发条件、输出格式和上游来源已统一整理。
- 带浏览器、登录态、Node、Playwright 或外部素材库的重型 Skill，不自动安装依赖或读取账号。
- 不提交 Cookie、Token、浏览器状态、NotebookLM 登录信息或用户隐私数据。
- 上游更新先审查，不自动执行第三方安装脚本。
