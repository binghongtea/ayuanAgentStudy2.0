from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage

# 1.创建模型的客户端
llm = ChatTongyi(
    model="qwen3-max"
)

# 2.准备上下文 + 当前用户消息
chat_history = [
    SystemMessage(content="背景设定：你现在是一个AI老师，负责上AI课程。"),
    HumanMessage(content="你是谁？")
]

# 3.携带上下文去调用模型
result = llm.invoke(input=chat_history)

# 4.处理输出
print(type(result))
print(result)
print(result.content)