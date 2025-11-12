# agents/supervisor.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from .f_agent import flight_node
from .gen_agent import guide_node

class AgentState(TypedDict):
    messages: List[BaseMessage]

# 创建工作流
workflow = StateGraph(AgentState)

# 添加节点
workflow.add_node("flight", flight_node)
workflow.add_node("guide", guide_node)
workflow.add_node("supervisor", lambda state: state)  # 主管就是最终输出

# 设置入口
workflow.set_entry_point("supervisor")

# 主管决定下一步
def supervisor_route(state):
    last_message = state["messages"][-1].content
    if any(k in last_message for k in ["机票", "航班"]):
        return "flight"
    elif any(k in last_message for k in ["攻略", "行程", "玩"]):
        return "guide"
    else:
        return END

workflow.add_conditional_edges("supervisor", supervisor_route)
workflow.add_edge("flight", END)
workflow.add_edge("guide", END)

app = workflow.compile()