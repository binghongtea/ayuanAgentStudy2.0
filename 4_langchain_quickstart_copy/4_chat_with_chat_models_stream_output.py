from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage


# 1.创建模型客户端
llm = ChatTongyi(
    model="qwen3-max",
    streaming=True
)

# 2.准备上下文 + 当前用户消息
chat_history = [
    SystemMessage(content="背景设定：你现在是一个AI辅助老师，用来辅助 story maker 授课"),
    HumanMessage(content="你是谁？")
]

# 3.携带上下文去调用模型
result = llm.stream(input=chat_history)

# 4.处理输出
for chunk in result:
    print(chunk.content, end='', flush=True)