# 第三方 Skill 安全边界

本套件整合第三方开源 Skill，但默认遵循以下边界：

1. 不自动执行 `curl | bash`、远程安装脚本、未知二进制文件或提权命令。
2. 不提交 Cookie、Token、API Key、NotebookLM 浏览器状态、账号会话或个人资料库内容。
3. NotebookLM、LinkedIn、小红书、X 等需要登录态的能力，只在用户明确要求且本地环境已配置时调用。
4. 第三方脚本运行前先检查目标文件、写入目录、网络域名和依赖列表。
5. 图像类 Skill 只在用户要求生成图片时调用图像工具；不把用户原图上传到未说明的第三方服务。
6. 不自动覆盖已有文章、图片、HTML 或项目资产；输出使用独立目录和新文件名。
7. 上游仓库更新不自动合并。更新前比较 `SKILL.md`、脚本、依赖和网络访问变化。
8. 外部事实、新闻、价格、政策、产品版本和模型动态必须重新联网核实，不能把 Skill 中的示例数据当成当前事实。

## 重型依赖提示

- `creator-notebooklm`：可能使用浏览器自动化并保存本地登录状态。
- `creator-punk-cover`：完整上游版本依赖风格库和图像生成工具。
- `creator-guizang-cards`：完整上游版本可能使用 Node.js、Playwright、网络图片源和 HTML 渲染脚本。
- `creator-baoyu-infographic`：需要可用的位图图像生成后端。
- `creator-html-publisher`：复杂预览或导出可能需要 Node.js 环境。

这些依赖不会因本套件被提交到 GitHub 而自动执行。
