import sys

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

# 1. 创建模型客户端
llm = ChatTongyi(model="qwen3-max")


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


# 2.2 绑定工具
tools = [get_weather, search_flights]
tools_map = {t.name: t for t in tools}
model_with_tools = llm.bind_tools(tools=tools)


# 3. 调用模型
messages = []
# user_input = "北京明天天气怎么样？另外帮我查一下北京到上海的航班。"
user_input = "北京明天天气怎么样？另外帮我查一下北京到上海的航班。【一次只能调用一个 tools 工具】"
# user_input = "北京明天天气怎么样？"
messages.append(HumanMessage(content=user_input))

result = model_with_tools.invoke(messages)
messages.append(result)
# print(result.tool_calls)


# 4. 根据 tool_calls 调用工具
if not result.tool_calls:
    # 没有需要调用的工具，直接输出并退出
    print("没有需要调用的工具")
    print(result.content)
    sys.exit(0)

# 有 tool_calls，逐个执行
for tool_call in result.tool_calls:
    tool_name = tool_call.get("name")
    tool_args = tool_call.get("args", {})
    tool_id = tool_call.get("id")

    tool_func = tools_map.get(tool_name)

    if tool_func:
        try:
            tool_result = tool_func.invoke(tool_args)
            print(f"调用工具 '{tool_name}' 成功，结果: {tool_result}")

            # 创建 ToolMessage 并将结果添加到消息历史
            tool_message = ToolMessage(
                content=tool_result,
                tool_call_id=tool_id
            )
            messages.append(tool_message)

        except Exception as e:
            print(f"调用工具 '{tool_name}' 失败: {e}")
            tool_message = ToolMessage(
                content=f"工具调用失败: {str(e)}",
                tool_call_id=tool_id
            )
            messages.append(tool_message)
    else:
        print(f"未找到工具: {tool_name}")
        tool_message = ToolMessage(
            content=f"未找到工具: {tool_name}",
            tool_call_id=tool_id
        )
        messages.append(tool_message)

# 在这里打印 messages
print("===== messages 内容 =====")
for i, msg in enumerate(messages):
    print(f"\n--- [{i}] {type(msg).__name__} ---")
    print(msg)

result = model_with_tools.invoke(messages)
print(result)
"""
tool_calls=[{'name': 'search_flights', 'args': {'from_city': '北京', 'to_city': '上海'}, 'id': 'call_abc2bd3c6b8d45cca110c645', 'type': 'tool_call'}] 

"""