from langchain_community.embeddings import DashScopeEmbeddings
import numpy as np

def euclidean_distance(a, b):
    """计算欧氏距离"""
    return np.linalg.norm(np.array(a) - np.array(b))

# 1.创建嵌入模型对象
embedding = DashScopeEmbeddings()

# 2.向量化
v1 = embedding.embed_query("我喜欢的水果是苹果")
v2 = embedding.embed_query("苹果是我最喜欢的水果")
v3 = embedding.embed_query("今天股市大涨")
print(euclidean_distance(v1, v2))
print(euclidean_distance(v1, v3))
print(euclidean_distance(v2, v3))