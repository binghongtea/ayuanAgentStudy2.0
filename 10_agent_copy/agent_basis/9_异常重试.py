import time

from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage

# 1.创建 tool
@tool
def get_weather(location: str) -> str:
    """
    获取某个位置的天气信息
    :param location: 地理位置
    :return: 天气情况
    """
    if location == '北京':
        raise Exception("发生错误啦~")
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

# ========== 2. 定义错误处理中间件（支持重试） ==========
@wrap_tool_call
def handle_tool_errors(request, handler):
    """使用自定义消息处理工具执行错误，支持最多重试3次。"""
    max_retries = 3
    retry_delay = 1  # 每次重试间隔（秒）

    last_exception = None

    for attempt in range(max_retries):
        try:
            # 尝试执行工具
            return handler(request)
        except Exception as e:
            last_exception = e
            print(f"工具执行失败（第 {attempt + 1}/{max_retries} 次尝试）: {e}")

            # 如果不是最后一次尝试，等待后继续重试
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            else:
                # 最后一次尝试仍失败，返回错误消息
                print(f"工具执行失败，已重试 {max_retries} 次，放弃。")
                return ToolMessage(
                    content=f"工具错误：请检查您的输入并重试。（{str(last_exception)}）",
                    tool_call_id=request.tool_call["id"]
                )


agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=tools,
    system_prompt="你是一个有好的出行助手,可以查询天气和航班信息",
    middleware=[handle_tool_errors]
)

# 3. 调用 agent 去帮我们们查询信息
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "北京明天天气怎么样？"}
    ]
})

# 4.打印结果
print(type(result)) # <class 'dict'>

print('\n' + '=' * 20)
for msg in result['messages']:
    print(f"消息类型：{type(msg).__name__}，消息内容：{msg}")