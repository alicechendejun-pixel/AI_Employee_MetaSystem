# 👑 AI Employee Meta-System (数字员工元帅系统)

This repository serves as the central command and registry interface for the CEO's local AI Employee Meta-System. It is designed so that external AIs (Claude, GPT, etc.) can read this repository to understand the local agentic architecture and invoke local tools.

## 🏗️ Architecture

- **`CEO_Launcher.py` & `Start_AI_Task.bat`**: The dynamic dispatcher that accepts plain-text commands, injects the AI Constitution, and physically launches background processes (e.g., MetaGPT, crewAI).
- **`AI_Skills_Registry.md`**: The master directory of all 20+ locally installed AI skill repositories (mounted as git submodules or local directories).
- **`.ai_system_prompt.md`**: The "AI Constitution" that enforces anti-ban mechanisms (429 handling) and autonomous tool usage.
- **`99_System_Docs_系统文档/`**: Strategic design documents and execution checklists.

## 🤖 Prompt for External AI Agents
If you are an external AI reading this repository to assist the CEO, you **MUST**:
1. Read `.ai_system_prompt.md` to understand your operational constraints.
2. Parse `AI_Skills_Registry.md` to discover which local engines (n8n, Dify, MetaGPT, etc.) are available for routing tasks.
3. NEVER generate unhandled "bare" HTTP requests. Always utilize the existing tools or implement robust backoff mechanisms.
