import os
import sys
from openai import OpenAI

# 创建模型客户端
client = OpenAI(
    api_key="sk-ws-H.PMXDEHX.s4SS.MEQCIGBjfTouZ_9SR79vSTRGYC1ACKnROW1rYzDFA27MacVrAiBQMIaMCrVA-OXK7DRQprVN5c4MzZps9uty7iVnvfxmww",
    base_url="https://ws-pztc39pf81j17w69.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 初始化对话历史
messages = []

print("=" * 50)
print("AI 助手已启动！输入 'exit' 或 'quit' 退出对话")
print("=" * 50)


# while 循环实现持续对话
while True:
    # 获取用户输入
    user_input = input("\n你：")

    # 退出条件
    if user_input.lower() in ['exit', 'quit', '退出']:
        print("再见！")
        break

    # 添加用户消息到历史
    messages.append({'role': 'user', 'content': user_input})

    # 调用模型
    try:
        completion = client.chat.completions.create(
            model="qwen3.8-max",
            messages=messages,
            stream=True
        )

        full_response = ''
        print("AI：", end='', flush=True)

        for chunk in completion:
            if chunk.choices:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end='', flush=True)
                    full_response += content

        print()

        # 将完整的回复保存到历史记录
        if full_response:
            messages.append({'role': 'assistant', 'content': full_response})

    except Exception as e:
        print(f"\b出错啦！{e}")
        sys.exit(1)