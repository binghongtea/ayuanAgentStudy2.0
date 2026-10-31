# ========== 对话类 ==========
from langchain_community.chat_models import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from memory import Memory


class ChatSession:
    def __init__(self, chat_session_id: str, system_prompt: str = "你是一个友好的AI助手"):
        self.chat_session_id = chat_session_id
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{user_input}")
        ])
        self.llm = ChatTongyi(model="qwen3-max", streaming=True)
        self.parser = StrOutputParser()
        self.memory = Memory()
        self.chain = self.prompt | self.llm | self.parser

    def send(self, user_input: str):
        # 1.准备上下文
        chat_history = self.memory.messages(self.chat_session_id)

        # 2.调用模型
        stream = self.chain.stream(input={
            "chat_history": chat_history,
            "user_input": user_input
        })

        # 3.解析输出
        full_reply = ""
        for chunk in stream:
            full_reply += chunk
            yield chunk

        self.memory.add_human_message(self.chat_session_id, user_input)
        self.memory.add_ai_message(self.chat_session_id, full_reply)


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
