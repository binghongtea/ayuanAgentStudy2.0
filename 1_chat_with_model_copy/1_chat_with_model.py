import os
from openai import OpenAI

# =========================
# 演示：和模型交互（一次交互）
# =========================

# 1.创建模型客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-2sjwh52zgwyaqnlv.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 2.访问模型（调用模型）
completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {'role': 'user', 'content': '你好，我是Story Maker，我是一个 AI 老师。'}
    ]
)

# 3.打印模型输出
print(completion.choices[0].message.content)