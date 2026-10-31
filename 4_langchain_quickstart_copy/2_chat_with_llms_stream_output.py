import os

from langchain_community.llms.tongyi import Tongyi

# 1.创建模型客户端
llm = Tongyi(
    model="qwen-max",
    api_key=os.environ['DASHSCOPE_API_KEY']
)
# 2.调用（流式输出）
result = llm.stream(input="你是谁")

# 3. 处理输出
for chunk in result:
    print(chunk, end='', flush=True)