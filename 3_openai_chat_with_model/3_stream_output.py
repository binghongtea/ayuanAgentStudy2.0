import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为: api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，各地域的URL不同。调用时请将{WorkspaceId}替换为真实的业务空间ID。
    base_url="https://ws-40hanr2q7t950wml.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-max",  # 模型列表: https://help.aliyun.com/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}
    ],
    stream=True,
    stream_options={"include_usage": True}
)

for chunk in completion:
    # print(chunk.model_dump_json())
    # print(chunk.choices[0].delta.content)
    # print(chunk.choices[0].delta.content, end='', flush=True)
    if chunk.choices:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end='', flush=True)
    elif hasattr(chunk, 'usage') and chunk.usage:
        print(f"\n\nToken使用情况：{chunk.usage}")
