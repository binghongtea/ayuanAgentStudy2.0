from langchain_community.chat_models import ChatTongyi
from langchain.tools import tool
from langchain.messages import ToolMessage
from langchain_openai import ChatOpenAI

# 1. 创建模型客户端
llm = ChatOpenAI(
    model='qwen3.8-max-0902',
    base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
# 2. 给 LLM 添加工具
@tool
def get_weather(location: str) -> str:
    """
    获取某个位置的天气信息
    :param location: 地理位置
    :return: 天气情况
    """
    return f"{location}的天气是100摄氏度，请你准备防晒。"


@tool
def search_flights(from_city: str, to_city: str) -> str:
    """
    查询两个城市之间的航班信息
    :param from_city: 出发城市
    :param to_city: 到达城市
    :return: 航班列表
    """
    if from_city == "北京" and to_city == "上海":
        return "北京 → 上海：CA1501 08:00-10:15 价格1200元；MU5102 13:30-15:45 价格980元"
    return f"抱歉，暂无 {from_city} 到 {to_city} 的航班信息。"


# 3. 绑定工具到 LLM
tools = [get_weather, search_flights]
model_with_tools = llm.bind_tools(tools=tools)

# 4. 调用模型
# user_input_1 = "北京明天天气怎么样？"
user_input_2 = "北京明天天气怎么样？另外帮我查一下北京到上海的航班。"
messages = [
    ("system", "你是一个友好的出行助手，可以查询天气和航班信息。"),
    ("human", f"{user_input_2}")
]

result = model_with_tools.invoke(messages)
print(type(result))  # <class 'langchain_core.messages.ai.AIMessage'>
print(result)
"""
tool_calls=[
{'name': 'get_weather', 'args': {'location': '北京'}, 'id': 'call_9658c958d2d44ad3869d5b10', 'type': 'tool_call'}
] 

 tool_calls=[
 {'name': 'get_weather', 'args': {'location': '北京'}, 'id': 'call_8dcfbea07d4f48b5a0a8a74e', 'type': 'tool_call'}, 
 {'name': 'search_flights', 'args': {'from_city': '北京', 'to_city': '上海'}, 'id': 'call_d730890e9b674e7db795c4dd', 'type': 'tool_call'}
 ]

"""