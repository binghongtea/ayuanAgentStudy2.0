from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.tools import tool
from agent import create_agent
from langchain_core.messages import HumanMessage


@tool
def get_weather(location: str) -> str:
    """查询天气信息"""
    return f"今天{location}的温度是 100℃"


@tool
def multiply(a: int, b: int) -> str:
    """将 a 和 b 相乘"""
    return str(a * b)


model = ChatTongyi(model="qwen-max")
tools = [get_weather, multiply]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="你是一个智能助手，可以查询天气和进行数学计算。"
)


# result = agent.invoke({
#     "messages": [HumanMessage(content='你好，我是maker')]
# })
# print("助手:", result['messages'][-1].content)
#
# result = agent.invoke({
#     "messages": [HumanMessage(content='你好，我是谁')]
# })
# print("助手:", result['messages'][-1].content)


# 循环问问题
messages = []
while True:
    user_input = input("你: ")
    if user_input == "exit":
        break

    messages.append(HumanMessage(user_input))
    result = agent.invoke({"messages": messages})
    messages = result["messages"]
    print("助手:", messages[-1].content)
