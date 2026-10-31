import os

from langchain_community.llms.tongyi import Tongyi

# 1.创建模型客户端
llm = Tongyi(
    model="qwen-max",
    api_key=os.environ['DASHSCOPE_API_KEY']
)
# 2.调用
result = llm.invoke(input="你是谁？")
# 3.输出处理
print(type(result))
print(result)