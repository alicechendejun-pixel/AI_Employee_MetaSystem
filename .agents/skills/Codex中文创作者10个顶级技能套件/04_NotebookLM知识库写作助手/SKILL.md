---
name: creator-notebooklm
description: 基于 Google NotebookLM 私有知识库进行检索、问答和内容写作。用于课程、书籍摘录、访谈、会议纪要、研究资料和用户自有文档；强调只依据资料回答、标明证据边界、减少幻觉，并在需要时调用上游 NotebookLM 自动化脚本。
metadata:
  short-description: NotebookLM 知识库检索与写作
---

# 04｜NotebookLM 知识库写作助手

## 定位

当内容必须基于用户已有课程、访谈、书籍、会议纪要、研究文档或资料库时，优先从 NotebookLM 获取有出处的答案，再进行写作。禁止凭模型记忆填补资料中不存在的事实。

## 触发场景

- 用户明确提到 NotebookLM 或提供 NotebookLM 链接
- “根据我的资料库写”“查一下我上传的文档”
- 从课程、会议、访谈或书籍笔记生成文章
- 需要引用原始材料、核对说法或减少幻觉

## 标准流程

### 1. 确定资料范围

- 使用哪个 Notebook
- 要回答的问题
- 输出用途：摘要、提纲、文章、脚本、事实核查
- 是否必须保留原文引用和出处

### 2. 查询资料库

如果完整上游脚本已经安装，始终通过其 `scripts/run.py` 包装器执行，不直接运行内部脚本：

```bash
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "问题" --notebook-id NOTEBOOK_ID
```

若当前套件目录中没有上游脚本，不假装已连接 NotebookLM。明确说明需要从上游仓库安装运行依赖：

```text
PleasePrompto/notebooklm-skill
```

### 3. 追问直到材料完整

第一轮答案后检查：

- 是否覆盖用户原问题的全部部分
- 是否缺时间、人物、数字、定义或因果关系
- 是否需要反例或原文上下文
- 是否把资料中的观点误当成事实

有缺口时继续向 NotebookLM 提问，再统一综合。

### 4. 写作时区分四类信息

- `[资料事实]`：资料明确记载
- `[资料观点]`：某位作者或受访者的判断
- `[作者判断]`：用户或文章要表达的观点
- `[待核实]`：资料不足，不能下结论

默认不把这些标签全部显示在成稿里，但在研究笔记和事实核查阶段必须区分。

## 安全边界

- 登录必须由用户在可见浏览器中亲自完成。
- 不要求用户在聊天中发送 Google 密码。
- Cookie、浏览器状态、Notebook 列表和认证文件不得提交到 Git。
- 不自动清除或删除 Notebook。
- 不把 NotebookLM 的回答当成绝对真相；重要事实仍应核对原始资料或权威来源。

## 输出模板

```markdown
# 资料库结论
# 证据与出处
# 仍然缺失的信息
# 可用于文章的观点结构
# 成稿或提纲
# 事实核查备注
```

## 上游来源

- Repository: `PleasePrompto/notebooklm-skill`
- Original skill: `SKILL.md`
- Upstream name: `notebooklm`
- Heavy dependencies: Python virtual environment, browser automation, local authentication state
