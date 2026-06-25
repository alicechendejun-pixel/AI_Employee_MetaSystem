---
name: creator-html-publisher
description: 将 Markdown、文章、研究报告、清单、数据和内容草稿转换为可直接打开、分享、截图或继续发布的单文件 HTML。用于公众号排版、文章网页、落地页、报告、海报、社交卡片和内容归档；强调响应式、中文排版、可读性和自包含交付。
metadata:
  short-description: Markdown 转可发布 HTML 成品
---

# 10｜HTML 发布与成品排版（HTML Anything）

## 定位

Markdown 是写作中间态，HTML 是读者看到的成品。本 Skill 负责内容生产线的最后一公里：把终稿变成无需构建、双击可看、便于复制和截图的单文件 HTML。

## 触发场景

- “做成 HTML”“把 Markdown 排版成网页”
- 公众号文章预览、长文网页、报告和内容归档
- 落地页、文章海报、社交卡片和数据展示
- 用户要求单文件、可下载、可直接打开的发布成品

## 默认交付标准

- 一个主要 `.html` 文件
- CSS 与必要脚本尽量内联
- 无构建步骤即可打开
- 桌面与手机均可阅读
- 中文字体、行高、段距和标题层级明确
- 保留原始事实、链接、表格、代码和引用
- 不依赖用户本机的绝对文件路径

## 工作流

### 1. 识别内容类型

判断是：

- 长文章 / 杂志式阅读
- 研究报告 / 数据报告
- 产品落地页
- 清单 / 方法论 / One-pager
- 海报 / 小红书 / 社交卡片
- 简历 / 作品集

不要用同一个网页模板处理所有内容。

### 2. 建立信息架构

先确定：

- 页面目的和主要读者
- 主标题、副标题和摘要
- 章节顺序
- 重点数据、引用、表格、图片和 CTA
- 哪些内容需要目录、脚注或来源区

### 3. 选择视觉系统

根据内容选择一种主视觉：

- Editorial Magazine：长文、观点、文化、人物和故事
- Swiss Grid：工具、数据、产品、方法和教程
- Parchment / Reading：报告、读书笔记、知识文档
- Poster：短内容、巨型标题和视觉传播
- Dashboard：指标、表格和数据复盘

坚持一种字体系统、间距尺度和色彩逻辑。

### 4. 编写单文件 HTML

建议结构：

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>...</title>
  <style>/* 全部页面样式 */</style>
</head>
<body>
  <main>...</main>
</body>
</html>
```

优先使用语义标签：`article`、`header`、`nav`、`section`、`figure`、`blockquote`、`table`、`footer`。

### 5. 中文排版规则

- 正文行宽控制在舒适阅读范围，不铺满超宽屏。
- 正文行高通常 1.7-1.9；段落之间留足空间。
- 标题不孤立在页面底部。
- 中英文、数字和标点保持一致的视觉节奏。
- 表格在手机端允许横向滚动，不压缩到不可读。
- 引用、脚注和来源区视觉弱于正文但仍清晰。
- 不用大量渐变、发光和无意义动画遮盖内容。

### 6. 资源与隐私

- 用户提供的本地图片优先复制到相对路径资源目录，或在用户要求单文件时转为可控的内嵌资源。
- 不把 API Key、Cookie、私人路径或内部文件内容嵌进 HTML。
- 外部字体、图片和脚本会影响离线使用；使用前说明依赖。

### 7. 检查

- HTML 能否直接打开？
- 手机宽度下是否溢出？
- 标题、表格、代码块和图片是否可读？
- 所有链接和锚点是否有效？
- 是否有错误事实、遗漏章节或残留占位符？
- 页面是否像成品，而不是开发调试界面？

## 输出目录

```text
html-output/{slug}/
├── index.html
├── assets/
└── README.md
```

用户明确要求单文件时，只交付 `index.html`，并把必要样式内联。

## 上游来源

- Repository: `nexu-io/html-anything`
- Upstream project: HTML Anything
- Upstream capabilities include multiple coding-agent CLIs, HTML templates and publishing/export workflows.
- 本适配层提供 Codex 可直接调用的中文内容发布工作流；复杂模板预览和平台导出可按需安装完整上游项目。
