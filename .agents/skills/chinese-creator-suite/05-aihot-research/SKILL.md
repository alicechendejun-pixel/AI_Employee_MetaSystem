---
name: creator-aihot-research
description: 中文 AI 热点、模型发布、产品动态、论文和行业事件研究。用于“今天 AI 圈发生了什么”“最近一周有什么模型发布”“OpenAI/Anthropic/Google 最新动态”等时效性问题；必须联网获取当前资料，不凭训练记忆回答。
metadata:
  short-description: AI 热点与深度研究工作台
---

# 05｜AI 热点与深度研究工作台（AI HOT）

## 定位

为 AI 内容创作者获取最新选题材料。默认先获取高质量精选，再补充原始来源、公司公告、论文和社区讨论，最后输出适合继续写作的选题包。

## 触发场景

- “今天 AI 圈有什么”“AI 日报”“最近 AI 新闻”
- “OpenAI / Anthropic / Google 最近发布了什么”
- “最近一周的 AI 模型、产品、论文、行业事件”
- 为公众号、小红书、YouTube 或 X 寻找 AI 热点选题

## 数据获取原则

1. 当前动态必须联网，不使用模型记忆替代检索。
2. 区分新闻发布日期与事件实际发生日期。
3. 优先原始来源：公司公告、官方博客、论文、发布说明、产品文档。
4. 聚合站只作为发现入口，重要结论回到原始来源核实。
5. 社区讨论用于判断争议和真实使用体验，不代替事实来源。

## AI HOT 公开接口

上游提供公开匿名 API。调用 `/api/public/*` 时设置浏览器 User-Agent：

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
```

### 默认：近期精选

```bash
curl -sH "User-Agent: $UA" \
  "https://aihot.virxact.com/api/public/items?mode=selected&take=50"
```

### 用户明确说“日报”

```bash
curl -sH "User-Agent: $UA" \
  "https://aihot.virxact.com/api/public/daily"
```

### 指定日期日报

```bash
curl -sH "User-Agent: $UA" \
  "https://aihot.virxact.com/api/public/daily/YYYY-MM-DD"
```

### 分类与关键词

常见分类：`ai-models`、`ai-products`、`industry`、`paper`、`tip`。

```bash
curl -sH "User-Agent: $UA" \
  "https://aihot.virxact.com/api/public/items?mode=selected&category=ai-models&take=50"

curl -sH "User-Agent: $UA" \
  "https://aihot.virxact.com/api/public/items?q=OpenAI&take=50"
```

接口失败时，不编造结果；改用公开网页和官方来源检索。

## 内容创作者输出

对每条候选热点给出：

```text
事件：
发生日期：
为什么重要：
原始来源：
中文读者最关心的角度：
可写成什么内容：
争议或待验证点：
时效等级：今天 / 本周 / 可做长期内容
```

## 选题筛选

优先保留：

- 对普通用户、创作者、企业或投资者有实际影响
- 存在明确变化、冲突、代价或机会
- 能找到一手证据
- 中文市场尚未被大量同质化搬运
- 用户能够加入自己的经验、判断或产品关联

不要只按“新闻最大”排序，要按“用户能否形成差异内容”排序。

## 输出格式

```markdown
# AI 热点简报
## 最重要的 3 件事
## 值得做内容的 5 个选题
## 每个选题的证据和原始来源
## 社区争议与真实使用反馈
## 今天不建议追的噪音
```

## 上游来源

- Repository: `KKKKhazix/khazix-skills`
- Original skill: `aihot/SKILL.md`
- Upstream name: `aihot`
- Service: `https://aihot.virxact.com`
