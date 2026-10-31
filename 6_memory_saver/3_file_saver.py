from langchain_community.chat_message_histories import FileChatMessageHistory

session_id = "123"
memory = FileChatMessageHistory(file_path=f"{session_id}_session_store.txt", encoding="utf-8")

memory.add_user_message("你是谁？")
memory.add_ai_message("我是AI？")

print(memory.messages)