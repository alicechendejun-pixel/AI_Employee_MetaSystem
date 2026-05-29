import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

# ==========================================
# 方案 3: CrewAI 高低端模型流水线 (系统级降额度打法)
# ==========================================
# 原理: “杀鸡焉用牛刀”。让免费、高额度的 Gemini 1.5 Flash 充当低级研究员，
# 负责去通读几十万字的 README 和源代码，并提取出 500 字的精简摘要。
# 然后，只把这 500 字发给最昂贵的 Claude 3.5 Sonnet（高级架构师），
# 让它运用“第一性原理”来做最终裁决。
# 这样，您在 Claude 上的额度消耗将降低 99%，并且完美避开封锁。
# ==========================================

# 1. 初始化模型 (需在环境变量中配置对应的 API KEY)
# 免费/高配额模型：负责干苦力
gemini_flash = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.3,
    google_api_key=os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_KEY")
)

# 昂贵/高智商模型：负责系统重构和顶层设计
claude_sonnet = ChatAnthropic(
    model="claude-3-5-sonnet-20240620", 
    temperature=0.7,
    anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", "YOUR_CLAUDE_KEY")
)

# 2. 定义 Agents (智能体)
junior_researcher = Agent(
    role='初级代码研究员',
    goal='快速通读庞大的开源项目代码和文档，过滤废话，提取核心运作逻辑。',
    backstory='你是一个不知疲倦的代码扫描器。你最擅长从成堆的垃圾数据中提取最核心的业务流。',
    verbose=True,
    allow_delegation=False,
    llm=gemini_flash  # 绑定低成本模型
)

senior_architect = Agent(
    role='第一性原理系统架构师',
    goal='基于初级研究员提供的简炼报告，运用 Elon Musk 的第一性原理重新审视商业和技术架构，指出可以删减和重构的部分。',
    backstory='你是一个冷酷、直接且一针见血的顶级架构师。你讨厌冗余，你的座右铭是“如果一个零件没有被经常要求加回来，说明你删得还不够多”。',
    verbose=True,
    allow_delegation=False,
    llm=claude_sonnet  # 绑定高智商模型
)

# 3. 定义 Tasks (任务)
task_read_code = Task(
    description='读取 500-AI-Agents-Projects 中的医疗行业 Agent 案例，将长达几万字的描述压缩为核心的 输入-处理-输出 (IPO) 模型流。',
    expected_output='一段 500 字以内的极简业务逻辑报告，只包含最核心的运转机制。',
    agent=junior_researcher
)

task_first_principles_review = Task(
    description='基于研究员的极简报告，使用第一性原理进行降维打击：指出这个医疗 Agent 商业模式中多余的环节，并设计一个直接切入利润池的 0-1 架构。',
    expected_output='一份冷酷、直接的第一性原理重构方案，重点指出“该删什么”。',
    agent=senior_architect
)

# 4. 组装 Crew 并启动
if __name__ == "__main__":
    print("=== 启动高低搭配智能体流水线 ===")
    my_crew = Crew(
        agents=[junior_researcher, senior_architect],
        tasks=[task_read_code, task_first_principles_review],
        process=Process.sequential # 顺序执行：Gemini 先看，提炼完给 Claude
    )
    
    # 开始执行
    result = my_crew.kickoff()
    
    print("\n==============================================")
    print("最终架构师 (Claude) 产出结果:")
    print("==============================================")
    print(result)
