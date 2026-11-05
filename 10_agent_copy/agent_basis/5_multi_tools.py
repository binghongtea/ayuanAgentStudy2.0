import sys

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
# 这文件是toolcalls并行多个tool
# 1. 创建模型客户端
llm = ChatOpenAI(
    model='qwen3.8-max-0902',
    base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 2. 给 LLM 添加工具
@tool
def get_weather(location:str) -> str:
    """
    获取某个位置的天气信息
    :param location: 地理位置
    :return:天气预报
    """
    return f"{location}的天气是100摄氏度，请你准备防晒"

@tool
def search_flights(from_city:str, to_city:str) -> str:
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
tools_map = {t.name : t for t in tools}
model_with_tools = llm.bind_tools(tools=tools)


# 3. 调用模型

messages = []
user_input = "北京明天天气怎么样？另外帮我查一下北京到上海的航班"
messages.append(HumanMessage(content=user_input))
result = model_with_tools.invoke(input = messages)
messages.append(result)

# 4. 根据 tool_calls 调用工具

if not result.tool_calls:
    print("没有需要调用的工具")
    print(result.content)
    sys.exit(0)

for tool_call in result.tool_calls:
    tool_name = tool_call.get("name")
    tool_args = tool_call.get("args")
    tool_id = tool_call.get("id")

    tool_func = tools_map.get(tool_name)

    if tool_func:
        try:
            tool_result = tool_func.invoke(tool_args)

            print('调用工具成功')
            # 创建ToolMessage
            tool_message = ToolMessage(content=tool_result,tool_call_id=tool_id)
            messages.append(tool_message)
        except Exception as e:
            print('调用工具失败')
            # 创建ToolMessage
            tool_message = ToolMessage(content='调用工具失败',tool_call_id=tool_id)
            messages.append(tool_message)
    else:
        print('未找到该工具')
        # 创建ToolMessage
        tool_message = ToolMessage(content='未找到该工具', tool_call_id=tool_id)
        messages.append(tool_message)

print('messages的内容')
for i,message in enumerate(messages):
    print(i,message)

# 5. 把结果提供给模型，得到最终回答
final_result = model_with_tools.invoke(input = messages)
print(final_result.content)






































