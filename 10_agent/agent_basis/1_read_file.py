from langchain_community.chat_models import ChatTongyi

# 1.创建模型客户端
llm = ChatTongyi(
    model="qwen3-max"
)

# 2.调用模型
result = llm.invoke(input=r"帮我读取我本地 E:\python\ai_learning\file\UFC.txt 的文件内容")

# 3.处理输出
print(type(result))
print(result.content)