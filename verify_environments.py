import os

base_dir = r"G:\我的云端硬盘\09-AI员工系统"

expected_repos = {
    "FinRobot": r"03_Wealth_Trading_搞钱与交易\FinRobot",
    "MakeMoneyWithAI": r"03_Wealth_Trading_搞钱与交易\MakeMoneyWithAI",
    "AI-Trader": r"03_Wealth_Trading_搞钱与交易\AI-Trader",
    "TradingAgents": r"03_Wealth_Trading_搞钱与交易\TradingAgents",
    "AutoHedge": r"03_Wealth_Trading_搞钱与交易\AutoHedge",
    "500-AI-Agents-Projects": r"03_Wealth_Trading_搞钱与交易\500-AI-Agents-Projects",
    "crewAI": r"04_Social_Network_社交与个人IP\crewAI",
    "n8n": r"04_Social_Network_社交与个人IP\n8n",
    "self-improvement-4all": r"05_Psychology_Improvement_心理建设教练\self-improvement-4all",
    "openclaw": r"05_Psychology_Improvement_心理建设教练\openclaw",
    "dify": r"06_Frameworks_Knowledge_底层架构与知识库\dify",
    "llama_index": r"06_Frameworks_Knowledge_底层架构与知识库\llama_index",
    "anything-llm": r"06_Frameworks_Knowledge_底层架构与知识库\anything-llm",
    "langchain": r"06_Frameworks_Knowledge_底层架构与知识库\langchain",
    "principles": r"07_First_Principles_第一性原理重构\principles",
    "awesome-ai-agents-2026": r"07_First_Principles_第一性原理重构\awesome-ai-agents-2026",
    "langgraph": r"08_System_Data_Engine_多智能体数据引擎\langgraph",
    "multi-agent-marketplace": r"08_System_Data_Engine_多智能体数据引擎\multi-agent-marketplace",
    "langflow": r"08_System_Data_Engine_多智能体数据引擎\langflow",
    "MetaGPT": r"08_System_Data_Engine_多智能体数据引擎\MetaGPT"
}

print("=== 目录与环境客观校验报告 ===")
valid_count = 0

for name, rel_path in expected_repos.items():
    full_path = os.path.join(base_dir, rel_path)
    if os.path.isdir(full_path):
        status = "已拉取"
        # 检查 Python 虚拟环境
        if os.path.isdir(os.path.join(full_path, "venv")):
            status += " | 包含 venv"
        # 检查 Node 项目特征
        elif os.path.isfile(os.path.join(full_path, "package.json")):
            status += " | Node 环境"
        print(f"[OK] {name:<25} -> {status}")
        valid_count += 1
    else:
        print(f"[FAIL] {name:<25} -> 目录不存在")

print("-" * 40)
print(f"总计找到库文件: {valid_count}/{len(expected_repos)}")
