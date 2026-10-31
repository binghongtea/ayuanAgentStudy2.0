import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-ws-H.PMXDEHX.s4SS.MEQCIGBjfTouZ_9SR79vSTRGYC1ACKnROW1rYzDFA27MacVrAiBQMIaMCrVA-OXK7DRQprVN5c4MzZps9uty7iVnvfxmww",
    base_url="https://ws-pztc39pf81j17w69.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}
    ],
    stream=True
)

for chunk in completion:
    # print(chunk.model_dump_json())
    if chunk.choices:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end='', flush=True)
    if hasattr(chunk, 'usage') and chunk.usage:
        print(f"\n\nToken消耗情况：{chunk.usage}")
