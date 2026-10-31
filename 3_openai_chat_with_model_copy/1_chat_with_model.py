import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为: api_key="sk-xxx",
    api_key="sk-ws-H.PMXDEHX.s4SS.MEQCIGBjfTouZ_9SR79vSTRGYC1ACKnROW1rYzDFA27MacVrAiBQMIaMCrVA-OXK7DRQprVN5c4MzZps9uty7iVnvfxmww",
    # 以下为华北2（北京）地域的URL，各地域的URL不同。调用时请将{WorkspaceId}替换为真实的业务空间ID。
    base_url="https://ws-pztc39pf81j17w69.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 用户 is not one of ['system', 'assistant', 'user', 'tool', 'function']
completion = client.chat.completions.create(
    model="qwen3.8-max",  # 模型列表: https://help.aliyun.com/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': '你是story maker的助手~'},
        {'role': 'user', 'content': '你是谁？'}
    ]
)

print(completion.choices[0].message.content)