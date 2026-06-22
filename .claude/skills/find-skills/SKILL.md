---
name: find-skills
description: 中文技能发现与安装助手。用户询问“有没有能完成某项任务的 Skill”“帮我找一个 Skill”“怎样扩展 Agent 能力”时，搜索、评估并给出可安装的 Agent Skill；优先选择官方、高安装量、持续维护且兼容当前平台的项目。
metadata:
  title_zh: 技能发现与安装
  language: zh-CN
  source_project: vercel-labs/skills
  source_url: https://github.com/vercel-labs/skills/tree/main/skills/find-skills
  adaptation: 中文标题与工作流适配版
  version: "1.0.0-zh"
---

# 技能发现与安装

用于从 GitHub、skills.sh 及兼容的 Agent Skill 生态中，找到适合当前任务的技能，并在安装前完成质量与安全核验。

## 何时调用

用户出现以下需求时使用：

- “帮我找一个能做 X 的 Skill。”
- “有没有适合 Claude Code、Codex、Gemini CLI、OpenClaw 的技能？”
- “这个任务有没有现成工具或工作流？”
- “给 Agent 增加网页操作、写作、设计、交易研究、测试或部署能力。”
- “把某个 GitHub Skill 安装到我的仓库。”

普通知识问答不必调用本 Skill；只有当任务可能通过可安装技能显著增强时才调用。

## 标准流程

### 1. 明确需求

先确定四项：

1. 任务领域：编程、设计、研究、营销、金融、自动化等。
2. 具体动作：生成、审查、抓取、部署、测试、分析或监控。
3. 使用平台：Claude Code、Codex、OpenClaw、Gemini CLI、Cursor 等。
4. 安装位置：全局、当前项目或指定 GitHub 仓库。

不要只根据一个宽泛关键词直接推荐。

### 2. 优先检查热门和官方来源

优先级从高到低：

1. 官方维护：Anthropic、Vercel、Microsoft、Google、GitHub 等。
2. 高安装量且持续维护的社区项目。
3. 有清晰许可证、测试和文档的专业作者项目。
4. 新项目或低安装量项目，仅在确有独特能力时列为备选。

常用入口：

```bash
npx skills find <关键词>
npx skills add <owner/repo@skill>
npx skills check
npx skills update
```

技能榜与详情页：`https://skills.sh/`

### 3. 安装前核验

至少检查：

- 来源仓库和作者是否可信。
- 最近是否维护，Issue 是否大量无人处理。
- 安装量、Star、Fork 及真实使用反馈。
- 是否包含脚本、网络访问、Shell 命令或写文件权限。
- 是否读取密钥、浏览器 Cookie、个人文件或系统目录。
- 许可证是否允许复制、修改和再分发。
- 是否与当前 Agent 和操作系统兼容。

禁止仅因“排名靠前”就跳过安全检查。

### 4. 给出清晰结果

每个候选项必须说明：

- 中文名称和原始 Skill 名。
- 解决什么问题。
- 来源仓库。
- 适用平台。
- 安装命令。
- 主要权限和风险。
- 推荐等级及理由。

默认只给 1—3 个最匹配选项，避免堆砌几十个仓库。

### 5. 执行安装

只有用户明确要求安装时，才执行写入或安装动作。

常见安装命令：

```bash
# 安装到当前项目
npx skills add owner/repo@skill -y

# 安装到用户全局目录
npx skills add owner/repo@skill -g -y
```

写入 GitHub 仓库时：

1. 保留原始 `name`，避免触发失效。
2. 中文标题放在 Markdown 一级标题或 `metadata.title_zh`。
3. 记录原始来源、许可证和修改说明。
4. 优先通过独立分支和 Pull Request 写入。
5. 安装后核对文件路径和 YAML frontmatter。

## 推荐输出格式

```markdown
### 中文名称（原名：skill-name）
- 用途：
- 来源：owner/repo
- 热度与维护：
- 兼容平台：
- 安装命令：
- 权限/风险：
- 推荐结论：
```

## 安全边界

- 不自动运行来源不明的 Shell、PowerShell 或 Python 脚本。
- 不把 Token、API Key、Cookie 或密码写入仓库。
- 不静默安装全局依赖。
- 不把“有很多 Star”当成安全证明。
- 涉及金融、医疗、法律和账户操作时，Skill 只能增强流程，不能替代专业判断和权限确认。

## 无匹配技能时

明确说明没有找到足够可靠的现成 Skill，然后给出两条路径：

1. 使用 Agent 当前能力直接完成任务。
2. 创建一个新的标准 `SKILL.md`，并定义触发条件、工作流、权限边界和验收标准。

不要为了给出答案而推荐低质量或不相关项目。
