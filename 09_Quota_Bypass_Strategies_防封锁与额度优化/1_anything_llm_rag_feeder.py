import os
import requests
import json
import glob

# ==========================================
# 方案 1: Anything-LLM 自动化 RAG 喂饭脚本
# ==========================================
# 原理: 通过 Anything-LLM 的开发者 API，将庞大的 500-AI-Agents 等项目代码
# 自动拆解并向量化存入本地数据库。
# 之后在 Claude Code 中提问时，通过调用 Anything-LLM 的对话接口，
# RAG 会自动截断 95% 无用的代码，只把最相关的 5% 发给 Claude/Gemini，
# 从而极大地降低每次对话的 Token 消耗，防止 5 小时额度被瞬间抽干。
# ==========================================

ANYTHING_LLM_API_URL = "http://localhost:3001/api"
# 您需要在 Anything-LLM 的 Settings -> API Keys 中生成一个 Key 并填入这里
API_KEY = "YOUR_ANYTHING_LLM_API_KEY_HERE"
# 您要在 Anything-LLM 中创建的工作区(Workspace)名称，例如 "ai-agents-knowledge"
WORKSPACE_SLUG = "ai-agents-knowledge"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def upload_document(file_path):
    """上传单个文件到 Anything-LLM 的内部存储"""
    print(f"正在上传文件: {file_path}")
    url = f"{ANYTHING_LLM_API_URL}/document/upload"
    
    with open(file_path, 'rb') as f:
        files = {'file': f}
        # Upload endpoint usually doesn't use Content-Type: application/json
        auth_header = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.post(url, headers=auth_header, files=files)
        
    if response.status_code == 200:
        return response.json().get("documents", [{}])[0].get("location")
    else:
        print(f"上传失败: {response.text}")
        return None

def update_workspace_embeddings(document_locations):
    """触发工作区将上传的文件进行向量化(Embedding)处理"""
    if not document_locations:
        return
        
    print(f"正在将 {len(document_locations)} 个文件注入工作区 {WORKSPACE_SLUG} 并开始向量化...")
    url = f"{ANYTHING_LLM_API_URL}/workspace/{WORKSPACE_SLUG}/update-embeddings"
    
    payload = {
        "adds": document_locations,
        "deletes": []
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("向量化成功！现在您的 Agent 可以从这个极低 Token 消耗的知识库中读取数据了。")
    else:
        print(f"向量化失败: {response.text}")

if __name__ == "__main__":
    print("=== 启动 Anything-LLM RAG 喂饭引擎 ===")
    
    # 目标：将超大项目里的 README 和 Markdown 全部提取出来，而不是一股脑塞给 Claude
    target_dir = r"G:\我的云端硬盘\09-AI员工系统\03_Wealth_Trading_搞钱与交易\500-AI-Agents-Projects"
    search_pattern = os.path.join(target_dir, "**", "*.md")
    
    md_files = glob.glob(search_pattern, recursive=True)
    print(f"找到 {len(md_files)} 个文档需要入库...")
    
    doc_locations = []
    for md_file in md_files:
        loc = upload_document(md_file)
        if loc:
            doc_locations.append(loc)
            
    # 一键触发向量化
    update_workspace_embeddings(doc_locations)
    
    print("\n[完成] 以后在 Claude Code 里，遇到这个仓库的问题，请先让 Agent 查询 Anything-LLM 接口。")
