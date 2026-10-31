# ========== 对话类 ==========
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from memory import Memory


class ChatSession:
    def __init__(self, session_id: str, system_prompt: str = "你是一个友好的AI助手。"):
        self.session_id = session_id
        self.memory = Memory()
        self.model = ChatTongyi(model="qwen3-max", streaming=True)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        self.parser = StrOutputParser()

        self.chain = self.prompt | self.model | self.parser

    def send(self, user_input: str):
        chat_history = self.memory.messages(self.session_id)

        stream = self.chain.stream({
            "chat_history": chat_history,
            "input": user_input
        })

        full_reply = ""
        for chunk in stream:
            full_reply += chunk
            yield chunk

        self.memory.add_human_message(self.session_id, user_input)
        self.memory.add_ai_message(self.session_id, full_reply)

# ========== 测试代码 ==========
if __name__ == "__main__":
    session = ChatSession("user_001")

    print("用户: 你好，我叫阿苑")
    print("AI: ", end='', flush=True)
    for chunk in session.send("你好，我叫阿苑"):
        print(chunk, end='', flush=True)
    print()

    print("用户: 我叫什么名字？")
    print("AI: ", end='', flush=True)
    for chunk in session.send("我叫什么名字？"):
        print(chunk, end='', flush=True)
    print()