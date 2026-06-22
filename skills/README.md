# Top Agent Skills

本目录保存从公开 GitHub 仓库引入的 Agent Skills 快照。

## 已加入

1. `find-skills`：发现、筛选和安装其他 Agent Skills。
2. `frontend-design`：生成具有明确审美方向、避免模板化的前端设计。
3. `vercel-react-best-practices`：React 与 Next.js 性能优化规则。

## 目录

```text
skills/
├── find-skills/SKILL.md
├── frontend-design/
│   ├── SKILL.md
│   └── LICENSE.txt
└── vercel-react-best-practices/SKILL.md
```

## 上游来源

- find-skills: `vercel-labs/skills/skills/find-skills`
- frontend-design: `anthropics/skills/skills/frontend-design`
- vercel-react-best-practices: `vercel-labs/agent-skills/skills/react-best-practices`

这些文件保留上游名称、描述和许可信息。需要在本地 Agent 环境安装完整最新版时，可运行：

```bash
npx skills add vercel-labs/skills@find-skills -g -y
npx skills add anthropics/skills@frontend-design -g -y
npx skills add vercel-labs/agent-skills@react-best-practices -g -y
```

> 本仓库中的副本用于统一登记和审阅；上游项目更新后，需要重新同步。