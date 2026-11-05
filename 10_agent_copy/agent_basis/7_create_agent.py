from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


# 1.创建 tool
# 1. 创建 tool
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

# 2.创建智能体
tools = [get_weather, search_flights]

agent = create_agent(
    model=ChatOpenAI(
        model='qwen3.8-max-0902',
        base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    ),
    tools=tools,
    system_prompt='你是一个友好的出行助手，可以查询天气和航班信息'
)
# 3. 调用 agent 去帮我们们查询信息
result = agent.invoke({
    "messages":[
        {"role":'user','content':'北京明天天气怎么样？另外帮我查一下北京到上海的航班。'}
    ]
})
# 4.打印结果
print(type(result))
print(result)
print(result["messages"])
print(result["messages"][0])

print("\n" + '-' * 20)

for msg in result["messages"]:
    print(f'消息类型：{type(msg).__name__},消息内容  {msg}')