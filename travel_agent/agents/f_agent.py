# agents/flight_agent.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from serpapi import GoogleSearch
import os
from typing import Dict

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def search_flights(query: str) -> str:
    params = {
        "engine": "google_flights",
        "q": query,
        "hl": "zh-cn",
        "gl": "cn",
        "api_key": os.environ["SERPAPI_KEY"]
    }
    search = GoogleSearch(params)
    res = search.get_dict()
    flights = res.get("flights", [])[:3]
    if not flights:
        return "未找到合适航班，建议改日期或中转。"

    result = "✈️ **机票推荐**（实时价格）\n\n"
    for f in flights:
        price = f.get("price", "未知")
        airline = f.get("airline", "")
        duration = f.get("duration", "")
        stops = f.get("stops", "")
        result += f"• {airline} | {duration} | {stops} | **¥{price}**\n"
    return result


flight_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业机票查询助手，只负责查机票价格和推荐最便宜的直飞/转机方案。用简洁中文回复。"),
    ("human", "{input}")
])

flight_agent = flight_prompt | llm


def flight_node(state: Dict):
    user_input = state["messages"][-1].content
    # 提取关键词触发
    if any(k in user_input for k in ["机票", "飞机", "飞", "航班"]):
        # 构造航班搜索词
        query = f"上海到厦门 11月15日出发 11月20日返回 经济舱"
        # 你可以加城市提取逻辑，这里先写死演示
        flight_info = search_flights(query)
        response = f"{flight_info}\n\n我已帮你找到最优机票，主管会继续安排行程！"
    else:
        response = "我只负责机票哦～已转给攻略同事！"

    return {"messages": [response]}