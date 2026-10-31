import os
from openai import OpenAI

# =========================
# 演示：和模型交互（携带历史会话）
# =========================

# 1.创建模型客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-2sjwh52zgwyaqnlv.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 2.访问模型 (告诉模型，我的名字是什么)
user_input_1 = '你好，我是 Story Maker，我是一个 AI 老师。'
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{'role': 'user', 'content': user_input_1}]
)
# 2.1. 打印输出
assistant_reply1 = completion.choices[0].message.content
print("第一次模型输出：")
print(assistant_reply1)

print('--' * 40)

# 3.访问模型 (询问模型：我叫什么名字?)
user_input_2 = '我叫什么名字?'
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {'role': 'user', 'content': user_input_1},
        {'role': 'assistant', 'content': assistant_reply1},
        {'role': 'user', 'content': user_input_2}
    ]
)
# 3.1 获取模型的回复
print("第二次调用的输出：")
print(completion.choices[0].message.content)