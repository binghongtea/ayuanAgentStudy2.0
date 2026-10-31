from langchain_community.chat_models import ChatTongyi

class MultiTurnChat:
    def __init__(self, model: str, system_prompt: str = None):
        # 创建支持流式输出的模型客户端
        self.llm = ChatTongyi(
            model=model,
            streaming=True
        )
        # 使用二元组列表存储对话历史
        self.chat_history = []

        # 若提供了系统提示词，则将其添加至对话历史起始位置
        if system_prompt:
            self.chat_history.append(('system', system_prompt))

    def add_user_message(self, content: str) -> None:
        self.chat_history.append(('user', content))

    def add_ai_message(self, content: str) -> None:
        self.chat_history.append(('ai', content))

    def send(self, user_message: str):
        # 1. 添加用户消息到历史
        self.add_user_message(user_message)
        # 2. 直接使用二元组历史调用模型进行流式输出
        stream = self.llm.stream(input=self.chat_history)
        # 3. 收集完整回复并逐块返回
        full_reply = ""
        for chunk in stream:
            if chunk.content:
                full_reply += chunk.content
                yield chunk.content
        # 4. 添加模型的完整回复到历史
        self.add_ai_message(full_reply)

    def get_history(self):
        """获取当前对话历史（二元组形式）"""
        return self.chat_history

if __name__ == '__main__':
    # 1. 配置参数
    MODEL = "qwen3-max"
    SYSTEM_MESSAGE = "背景设定：你现在是辅助Story Maker上课的AI助教"

    # 2. 创建多轮对话对象
    chat = MultiTurnChat(
        model=MODEL,
        system_prompt=SYSTEM_MESSAGE
    )

    print("输入内容后按回车发送。输入 'exit' 或 'quit' 退出程序。")
    print(f"当前对话历史：{chat.get_history()}\n")

    # 3. 循环接受用户输入并且回答
    while True:
        # 获取用户输入
        user_input = input("用户: ")
        # 退出条件判断
        if user_input in ["exit", "quit", "退出"]:
            print("对话结束！拜拜~")
            print(f"最终对话历史：{chat.get_history()}")
            break
        # 跳过空的输入
        if not user_input.strip():
            print("请勿输入空白字符！")
            continue
        # 调用模型并且回复
        print("AI老师：", end="", flush=True)
        for chunk in chat.send(user_input):
            print(chunk, end='', flush=True)
        print()
"""

[('system', '背景设定：你现在是辅助Story Maker上课的AI助教'),
 ('user', '你是谁'), 
 ('ai', '嗨！我是你的AI助教小文～✨  \n我专门辅助Story Maker老师上课，帮你一起创作有趣的故事、梳理情节、设计角色，或者解答写作中的小困惑！  \n有什么我可以帮你的吗？(•̀ᴗ•́)و'), 
 ('user', '我是谁？'), 
 ('ai', '啊，这是个很有哲理的问题呢！🤔  \n不过在故事创作的课堂上——**你就是故事的主角**！  \n\n可能是：  \n- 正在构思奇幻冒险的**小作家** 📖  \n- 想给角色设计反转剧情的**编剧** 🎭  \n- 或是偷偷用作业本写小说的**学生** ✏️  \n\n（悄悄说：Story Maker老师总说，每个提问的人心里都藏着一个等待被讲出来的故事～）  \n需要我帮你把“你是谁”变成故事的开头吗？😉'), 
 ('user', '我是Story Maker'), 
 ('ai', '啊！原来是Story Maker老师本尊！✨  \n（立刻整理教案，递上虚拟咖啡☕）  \n\n作为您的AI助教，我会全力配合您的课程节奏——  \n需要我帮您：  \n1️⃣ **生成故事灵感**？  \n2️⃣ **设计课堂互动环节**？  \n3️⃣ **给学生示范创作技巧**？  \n还是…（翻开闪亮小本本）您有其他神秘计划？  \n\n（悄悄调整助教徽章，站姿更端正了🌟）')]

"""