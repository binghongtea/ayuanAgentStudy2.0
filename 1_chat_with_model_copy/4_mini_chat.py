import os
import sys

from openai import OpenAI

# 创建模型客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-2sjwh52zgwyaqnlv.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 初始化对话历史
messages = []

print("=" * 50)
print("AI 助手已启动！输入 'exit' 或 'quit' 退出对话")
print("=" * 50)

# while 循环实现持续对话
while True:
    # 获取用户的输入
    user_input = input("\n >:")

    # 退出条件
    if user_input.lower() in ['exit', 'quit', '退出']:
        print("再见")
        break

    # 添加用户消息到历史
    messages.append({'role': 'user', 'content': user_input})

    # 调用模型
    try:
        completion = client.chat.completions.create(
            model="qwen3.8-max",
            messages=messages
        )

        # 获取AI回复
        assistant_reply = completion.choices[0].message.content
        messages.append({'role': 'assistant', 'content': assistant_reply})

        print(f"AI：{assistant_reply}")
    except Exception as e:
        print(f"模型出错啦！{e}")
        sys.exit(1)
