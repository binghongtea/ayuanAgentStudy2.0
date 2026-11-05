import sys

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# 1. 创建模型客户端
llm = ChatOpenAI(
    model='qwen3.8-max-0902',
    base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
# 2. 工具定义
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


tools = [get_weather, search_flights]
tools_map = {t.name: t for t in tools}
model_with_tools = llm.bind_tools(tools=tools)


# 3. System Prompt
SYSTEM_PROMPT = """你是一个智能助手，可以调用工具来回答用户问题。

可用工具：
- get_weather(location): 获取某个位置的天气信息
- search_flights(from_city, to_city): 查询两个城市之间的航班信息

工作方式：
1. 每次回复只能调用一个工具，不要在同一条回复中调用多个工具。
2. 拿到工具结果后，再决定是否需要调用下一个工具。
3. 当信息足够时，直接给出最终回答，不要再调用工具。
"""


# 4. 主循环：有工具调用就执行，直到模型给出最终回答

def run_agent(user_input:str) -> str:
    """
    主循环，ReAct范式
    :param user_input: 用户输入问题
    :return: 执行结果
    """
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_input),
    ]

    step = 1
    while True:
        result = model_with_tools.invoke(input=messages)
        messages.append(result)
        # 如果没有工具调用，就直接返回结果
        if not result.tool_calls:
            print(f'最终回答{result.content}')
            return result.content

        for tool_call in result.tool_calls:
            tool_name = tool_call.get('name')
            tool_args = tool_call.get('args')
            tool_id = tool_call.get('id')

            tool_func = tools_map.get(tool_name)

            if tool_func:
                try:
                    tool_result = tool_func.invoke(tool_args)

                    print(f'{tool_name}调用成功')
                    tool_message = ToolMessage(
                        content=tool_result,
                        tool_call_id=tool_id,
                    )
                    messages.append(tool_message)
                except Exception as e:
                    print(f'{tool_name}调用失败{e}')
                    tool_message = ToolMessage(
                        content=f'{tool_name}调用失败',
                        tool_call_id=tool_id,
                    )
                    messages.append(tool_message)
            else:
                print(f'{tool_name}未找到')
                tool_message = ToolMessage(
                    content=f'{tool_name}未找到',
                    tool_call_id=tool_id,
                )
                messages.append(tool_message)

        step += 1

if __name__ == '__main__':
    run_agent('北京明天天气怎么样？另外帮我查一下北京到上海的航班。')