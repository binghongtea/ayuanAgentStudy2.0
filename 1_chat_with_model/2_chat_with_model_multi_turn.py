import os
from openai import OpenAI

# =========================
# 演示：和模型交互（多次交互）
# =========================

# 1.创建模型客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-2sjwh52zgwyaqnlv.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 2.访问模型 (告诉模型，我的名字是什么)
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{'role': 'user', 'content': '你好，我是Story Maker，我是一个 AI 老师。'}]
)
# 2.1. 打印输出
print("第一次模型输出：")
print(completion.choices[0].message.content)

print('--' * 40)

# 3.访问模型 (询问模型，我的名字是什么)
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{'role': 'user', 'content': '我叫什么名字？'}]
)
# 3.1. 打印输出
print("第二次模型输出：")
print(completion.choices[0].message.content)
