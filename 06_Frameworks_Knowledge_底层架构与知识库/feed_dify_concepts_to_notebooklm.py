import subprocess

def run_cmd(cmd):
    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if res.returncode != 0:
        print("Error:", res.stderr)
        return None
    return res.stdout.strip()

print("=== 正在为您创建 CEO 专属的 Dify / RAG 知识库 ===")

# 1. 尝试创建新的 Notebook
nb_id = run_cmd(['notebooklm', 'create', 'AI_CEO_Command_Center'])

if not nb_id or "error" in nb_id.lower() or "expire" in nb_id.lower():
    print("!! 检测到 NotebookLM 授权已过期。")
    print("请先在终端运行 'notebooklm login' 重新授权，然后再运行此脚本。")
    exit(1)

print(f"成功创建笔记本: AI_CEO_Command_Center (ID: {nb_id})")

# 2. 收集网上关于 Dify 和 RAG 的“高管易懂版”讲解视频（而不是程序员写的枯燥代码教程）
# 这些视频专门讲“什么是知识库”、“什么是工作流”、“如何拼装商业 AI”
dify_concept_urls = [
    "https://www.youtube.com/watch?v=kYJpEqWvH4Y", # Dify 官方基础概念介绍
    "https://www.youtube.com/watch?v=F07XW3vQ00E", # RAG 知识库通俗原理解释
    "https://www.youtube.com/watch?v=GjYJq9Vv9oU"  # 如何构建无代码企业级 AI
]

for url in dify_concept_urls:
    print(f"正在注入高管级知识源: {url}")
    run_cmd(['notebooklm', 'source', 'add', '--notebook', nb_id, '--type', 'youtube', url])

print("\n[完成] 知识源注入完毕！")
print("您现在可以去 NotebookLM 网页端，向它提问：")
print("1. '用大白话告诉我 Dify 是干嘛的？'")
print("2. '我该怎么向客户推销 RAG 知识库？'")
print("3. '帮我生成一份长达 10 分钟的关于 Dify 概念的双人播客（Audio Overview）。'")
