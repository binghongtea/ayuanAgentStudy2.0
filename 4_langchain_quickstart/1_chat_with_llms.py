import os

from langchain_community.llms.tongyi import Tongyi

# 1.创建模型的客户端
# qwen-max 是狭义的 llms，适合于单次调用
llm = Tongyi(
    model="qwen-max",
    api_key=os.environ['DASHSCOPE_API_KEY']
)

# 2.调用模型
result = llm.invoke(input="你是谁？")

# 3.处理输出
print(type(result))
print(result)