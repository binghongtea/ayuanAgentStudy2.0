import os
import sys
from openai import OpenAI

# 创建模型客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为: api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，各地域的URL不同。调用时请将{WorkspaceId}替换为真实的业务空间ID。
    base_url="https://ws-40hanr2q7t950wml.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
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

    # 调用模型（流式输出）
    try:
        completion = client.chat.completions.create(
            model="qwen3.8-max",
            messages=messages,
            stream=True  # 启用流式输出
        )

        # 收集AI回复（用于保存到历史记录）
        full_response = ""
        print("AI：", end='', flush=True)

        # 流式打印输出
        for chunk in completion:
            if chunk.choices:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end='', flush=True)
                    full_response += content

        print()  # 换行

        # 将完整的回复保存到历史记录
        if full_response:
            messages.append({'role': 'assistant', 'content': full_response})

    except Exception as e:
        print(f"\n出错了：{e}")
        sys.exit(1)