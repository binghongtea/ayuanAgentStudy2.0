from langchain_community.embeddings import DashScopeEmbeddings

# 1.创建嵌入模型对象
embedding = DashScopeEmbeddings()

# 2.向量化
vector = embedding.embed_query("你是谁？")

# 3.处理输出
print(vector)
print(len(vector))