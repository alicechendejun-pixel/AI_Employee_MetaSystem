# GitHub 热门前三 Agent Skill（中文版）

本目录已安装以下三个 Skill。为保持 Agent 自动识别能力，文件夹名和 YAML 中的 `name` 保留英文；面向用户的一级标题、描述和工作流采用中文。

## 1. 技能发现与安装

- **原名**：`find-skills`
- **路径**：`.claude/skills/find-skills/SKILL.md`
- **用途**：搜索、评估和安装新的 Agent Skill；安装前检查来源、维护状态、权限、许可证和平台兼容性。
- **上游来源**：`vercel-labs/skills`

## 2. 前端视觉设计

- **原名**：`frontend-design`
- **路径**：`.claude/skills/frontend-design/SKILL.md`
- **用途**：建立有辨识度的网页与应用视觉系统，处理色彩、字体、布局、动效、文案和可访问性，避免模板化 AI 设计。
- **上游来源**：`anthropics/skills`
- **许可证**：Apache License 2.0，许可证副本位于同目录 `LICENSE.txt`。

## 3. Vercel React 与 Next.js 最佳实践

- **原名**：`vercel-react-best-practices`
- **路径**：`.claude/skills/vercel-react-best-practices/SKILL.md`
- **用途**：优化 React/Next.js 的异步请求、Bundle、服务端性能、客户端请求、重复渲染和 JavaScript 执行效率。
- **上游来源**：`vercel-labs/agent-skills`
- **许可证**：MIT。

## 调用示例

```text
使用 find-skills，查找适合批量制作短视频的高质量 Skill，并先做安全审查。
```

```text
使用 frontend-design，为金融交易工具设计一套不模板化的中文落地页。
```

```text
使用 vercel-react-best-practices，审查这个 Next.js 项目的性能问题，按严重程度输出修改建议。
```

## 安装状态

- [x] 三个 `SKILL.md` 已写入 GitHub 仓库。
- [x] 中文标题与中文触发描述已完成。
- [x] 原始英文 Skill 名已保留。
- [x] 上游来源与修改说明已记录。
- [x] `frontend-design` 的 Apache 2.0 许可证已随文件保存。
