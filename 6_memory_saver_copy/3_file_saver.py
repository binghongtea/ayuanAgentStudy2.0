from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

chat_session_id = "123"
memory_saver = FileChatMessageHistory(
    file_path=f"{chat_session_id}_session_store.txt",
    encoding="utf-8",
)

# 2.添加消息
# memory_saver.add_user_message(HumanMessage(content="你是谁？"))
# memory_saver.add_ai_message(AIMessage(content="我是 qwen"))

# 3.打印消息列表
print(memory_saver.messages)