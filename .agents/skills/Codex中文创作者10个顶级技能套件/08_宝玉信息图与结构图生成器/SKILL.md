---
name: creator-baoyu-infographic
description: 将中文文章、流程、框架、清单、对比、时间线、方法论和数据转换为专业信息图。先分析信息结构，再选择布局与视觉风格，保存完整生图提示词，并使用当前环境可用的位图图像生成工具产出可发布图片。
metadata:
  short-description: 信息图、结构图与高密度视觉总结
---

# 08｜宝玉信息图与结构图生成器

## 定位

把复杂逻辑从“可读文字”转换成“可保存、可复用、可一眼理解”的视觉结构。布局负责信息关系，风格负责视觉语言，两者分开选择。

## 触发场景

- “做信息图”“把这段变成结构图”
- “流程、框架、方法论、时间线、对比、清单可视化”
- “做一张高密度信息大图”
- 为公众号、小红书、报告和课程生成视觉总结

## 信息结构选择

| 内容关系 | 推荐布局 |
|---|---|
| 时间与步骤 | `linear-progression` |
| A/B、前后、利弊 | `binary-comparison` |
| 多因素比较 | `comparison-matrix` |
| 层级和优先级 | `hierarchical-layers` |
| 分类体系 | `tree-branching` / `periodic-table` |
| 中心概念与分支 | `hub-spoke` |
| 组成和机制 | `structural-breakdown` |
| 多主题总览 | `bento-grid` |
| 表层与深层 | `iceberg` |
| 问题到解决 | `bridge` |
| 转化和筛选 | `funnel` |
| 指标和数据 | `dashboard` |
| 旅程和里程碑 | `winding-roadmap` |
| 循环系统 | `circular-flow` |
| 高密度指南 | `dense-modules` |

## 视觉风格

可根据内容选择：手工纸艺、技术蓝图、企业扁平、复古学术、粉笔板、粗线漫画、瑞士复古网格、莫兰迪手账、教育手绘、像素艺术等。默认只用一种主风格，避免风格词堆叠。

## 工作流

### 1. 忠实提取内容

- 保留原始事实、数字、顺序和关系。
- 不为画面好看擅自改写关键数据。
- 秘钥、Cookie、Token 和隐私信息必须先剔除。
- 内容过多时先决定学习目标和主视觉任务，再做取舍。

### 2. 建立结构化内容

```markdown
# 主题
## 读者看完要理解什么
## 核心节点
## 节点之间的关系
## 必须保留的数据
## 可删除的解释
## 风险与禁止项
```

### 3. 推荐组合

给出不超过 3 个“布局 × 风格”组合，并说明每个组合为什么适合。用户已明确指定或说“直接生成”时，不重复确认。

### 4. 编写并保存提示词

生成前必须把完整提示词保存到：

```text
infographic/{topic-slug}/prompts/infographic.md
```

提示词包含：画幅、语言、布局、视觉风格、信息层级、文字上限、数据、主体、色彩、负面约束和最终质量标准。

### 5. 生成位图

优先使用当前运行环境原生图像生成工具。没有位图生成后端时，明确说明依赖缺失；禁止偷偷用 SVG、HTML、Canvas 或程序化绘图冒充最终信息图。

中文文字错误时，优先减少图中文字或重新生成，不使用程序覆盖位图文字来伪装修复。

### 6. 保存交付

```text
infographic/{topic-slug}/
├── source.md
├── analysis.md
├── structured-content.md
├── prompts/infographic.md
└── infographic.png
```

## 质量检查

- 第一眼能否看出信息结构？
- 节点数量是否超过手机阅读承载量？
- 数据与原文是否一致？
- 字体是否清晰，中文是否过多？
- 装饰是否干扰逻辑？
- 是否适合目标平台比例？

## 上游来源

- Repository: `JimLiu/baoyu-skills`
- Original skill: `skills/baoyu-infographic/SKILL.md`
- Upstream name: `baoyu-infographic`
- Upstream version inspected: `1.117.4`
