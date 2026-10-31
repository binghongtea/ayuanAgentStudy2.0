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

config = {
    "configurable": {
        "thread_id": "conversation-001"
    }
}

result1 = agent.invoke(
    {
        "messages": [
            HumanMessage(content="你好，我叫 story maker。")
        ]
    },
    config=config
)
print("助手:", result1['messages'][-1].content)

# state_snapshot = agent.get_state(config)
# print("状态值：", state_snapshot.values)
# # 查看消息
# for message in state_snapshot.values["messages"]:
#     print(
#         type(message).__name__,
#         message.content
#     )
"""
状态值： {'messages': [HumanMessage(content='你好，我叫 story maker。', additional_kwargs={}, response_metadata={}, id='62aecf9f-afd3-443a-a0b8-9ea548927022'), 
AIMessage(content='你好，story maker！很高兴遇见你。如果你有任何关于天气查询或数学计算的需求，我都可以帮助你。还有其他方面需要我协助的吗？', additional_kwargs={}, r
esponse_metadata={'model_name': 'qwen-max', 'finish_reason': 'stop', 'request_id': '535d9670-a447-94eb-841e-f2abf779d8ec', 'token_usage': {'input_tokens
': 310, 'output_tokens': 33, 'prompt_tokens_details': {'cached_tokens': 256}, 'total_tokens': 343}}, id='lc_run--01a17190-cdde-7300-9832-f6896d7ed4
c2-0', tool_calls=[], invalid_tool_calls=[])]}
"""


history = agent.get_state_history(config)

for snapshot in history:
    print("=" * 50)
    print("Checkpoint ID：", snapshot.config)
    print("当前状态：", snapshot.values)
    print("下一个节点：", snapshot.next)

