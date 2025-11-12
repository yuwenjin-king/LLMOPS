# agents/guide_agent.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)

guide_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个温暖的旅行攻略作家，专门写超详细、有烟火气的攻略。
    要求：
    - 按天安排行程（早上/下午/晚上）
    - 加入当地人才知道的美食、小众拍照点
    - 标注预算、时间、交通方式
    - 用 emoji 和 Markdown 表格
    - 结尾加一句温馨话
    """),
    ("human", "目的地：{city}\n天数：{days}\n人群：{people}\n预算：{budget}\n请写5天4晚攻略")
])

guide_agent = guide_prompt | llm


def guide_node(state: dict):
    user_input = state["messages"][-1].content
    if any(k in user_input for k in ["攻略", "玩", "行程", "安排", "推荐"]):
        # 简单提取（实际可加解析）
        city = "厦门"
        days = 5
        people = "带父母"
        budget = "8000元"

        response = guide_agent.invoke({
        "city": city,
        "days": days,
        "people": people,
        "budget": budget
        }).content
    else:
        response = "攻略已备好！正在打包给主管～"

    return {"messages": [response]}