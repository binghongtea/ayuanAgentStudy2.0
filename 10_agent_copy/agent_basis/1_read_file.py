from langchain_openai import ChatOpenAI

# 1.创建模型客户端
llm = ChatOpenAI(
    model='qwen3.8-max-0902',
    base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 2.调用模型
result = llm.invoke(input=r"帮我读取我本地 E:\daima\ayuanAgentStudy2.0\file\UFC.txt 的文件内容")

# 3.处理输出
print(result)
print(type(result))
