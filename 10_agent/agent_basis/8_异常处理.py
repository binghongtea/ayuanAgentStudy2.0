from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import ToolMessage
from langchain.tools import tool


# ========== 1. 定义工具 ==========

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


# ========== 2. 定义错误处理中间件 ==========

@wrap_tool_call
def handle_tool_errors(request, handler):
    """使用自定义消息处理工具执行错误。"""
    try:
        return handler(request)
    except Exception as e:
        # 向模型返回自定义错误消息
        return ToolMessage(
            content=f"工具错误：请检查您的输入并重试。（{str(e)}）",
            tool_call_id=request.tool_call["id"]
        )


# ========== 3. 创建 Agent ==========

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_weather, search_flights],
    middleware=[handle_tool_errors]
)


# ========== 4. 调用 Agent ==========

if __name__ == "__main__":
    result = agent.invoke({
        "messages": [{"role": "user", "content": "明天北京天气如何？"}]
    })

    # 输出最终回复
    print("===== messages 内容 =====")
    for i, msg in enumerate(result["messages"]):
        print(f"\n--- [{i}] {type(msg).__name__} ---")
        print(msg)

    # print(result["messages"][-1].content)