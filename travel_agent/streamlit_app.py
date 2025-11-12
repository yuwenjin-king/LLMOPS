# streamlit_app.py
import streamlit as st
from agents.sub_agent import app as multi_agent
from langchain_core.messages import HumanMessage
import os

st.set_page_config(page_title="AI旅游多Agent助手", page_icon="✈️", layout="wide")
st.title("✈️ 小旅 · 多智能体旅游助手（机票+攻略）")

if "messages" not in st.session_state:
    st.session_state.messages = []
    intro = """
    哈喽！我是**小旅**，现在我有两位专业同事：
    - **机票专员**：实时查最便宜航班
    - **攻略作家**：写本地人才知道的深度攻略

    直接告诉我你的想法吧～
    """
    st.session_state.messages.append({"role": "assistant", "content": intro})

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("例如：上海飞厦门，11月15-20日，带父母玩5天，预算8000"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("小旅正在协调团队为你规划..."):
            inputs = {"messages": [HumanMessage(content=prompt)]}
            result = ""
            for output in multi_agent.stream(inputs):
                for key, value in output.items():
                    if "messages" in value:
                        msg = value["messages"][-1]
                        if isinstance(msg, str):
                            result += msg + "\n\n"
                        else:
                            result += msg.content + "\n\n"
            st.markdown(result)
        st.session_state.messages.append({"role": "assistant", "content": result})