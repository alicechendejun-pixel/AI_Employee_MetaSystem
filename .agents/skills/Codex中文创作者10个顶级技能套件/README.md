# Codex 中文创作者 10 个顶级 Skills 套件

这是一个集中管理的中文内容生产线，安装位置：

```text
.agents/skills/chinese-creator-suite/
```

Codex 会从仓库级 `.agents/skills/` 递归发现各子目录中的 `SKILL.md`。本套件按生产流程编号，避免 Skill 变成无法调用的收藏夹。

## 套件目录

| 顺序 | 中文标题 | Codex Skill 名称 | 上游仓库 | 核心用途 |
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
选题判断
  → 02 选题、Hook 与内容诊断
  → 05 最新热点与外部材料 / 04 私有知识库材料
  → 03 调研、提纲与正文
  → 01 去 AI 味与文风清洗
  → 06 封面 / 07 社交卡片 / 08 信息图 / 09 正文配图
  → 10 HTML 成品发布
```

## 最小高频组合

先跑这三个：

1. `creator-dbskill-editor`：判断内容值不值得做。
2. `creator-stop-slop`：清除 AI 写作痕迹。
3. `creator-punk-cover`：解决第一眼点击。

## 集成方式

- 每个子目录都是一个独立、可发现的 Codex Skill。
- 中文标题、触发条件、输出格式和上游来源已统一整理。
- 指令型 Skill 已直接集成主要工作流。
- 带浏览器、登录态、Node、Playwright 或外部素材库的重型 Skill，不会自动安装依赖或读取账号；首次实际运行时按对应 `SKILL.md` 的依赖检查执行。
- 不提交 Cookie、Token、浏览器状态、NotebookLM 登录信息或任何用户隐私数据。

## 调用示例

```text
使用 creator-dbskill-editor，判断这个选题是否值得做，并给出三个更强 Hook。

使用 creator-stop-slop，只去除 AI 味，不改变我的观点和事实。

使用 creator-research-writer，先调研并列出处，再写一篇公众号长文。

使用 creator-guizang-cards，把这篇文章拆成 6 张小红书卡片。

使用 creator-html-publisher，把最终稿做成一个可直接打开的单文件 HTML。
```

## 上游与更新

本目录是面向中文内容生产的 Codex 适配套件。每个 Skill 文件末尾均记录上游仓库和原始 Skill 路径。更新时先审查上游变更，不自动执行第三方安装脚本。
