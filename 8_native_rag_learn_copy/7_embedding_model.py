from langchain_community.embeddings import DashScopeEmbeddings

# 创建模型对象，默认使用 text-embedding-v1
embedding_model = DashScopeEmbeddings(
    model="qwen3.7-text-embedding"
)

user_input = "手机没电了，我需要充电"
result = embedding_model.embed_query(user_input)
print(type(result))
print(len(result))
print(result)