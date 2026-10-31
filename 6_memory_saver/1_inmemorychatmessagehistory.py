from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

# 1.创建 InMemoryChatMessageHistory 对象
memory_saver = InMemoryChatMessageHistory()

# 2.添加消息
memory_saver.add_user_message(HumanMessage(content="你是谁？"))
memory_saver.add_ai_message(AIMessage(content="我是 qwen"))

# 3.获取消息列表
print(memory_saver.messages)