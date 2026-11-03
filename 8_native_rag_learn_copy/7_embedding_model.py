from langchain_community.embeddings import DashScopeEmbeddings

# 创建模型对象，默认使用 text-embedding-v1
embedding_model = DashScopeEmbeddings(
    model='qwen3.7-text-embedding-flash'
)

# 向量化
user_input = '你好'
result = embedding_model.embed_query(user_input)
print(result)
print(type(result))
print(len(result))