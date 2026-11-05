from langchain_community.embeddings import DashScopeEmbeddings
import numpy as np


def cosine_similarity(vec1, vec2):
    """余弦相似度（值越大越相似）"""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


# 创建模型对象
embedding_model = DashScopeEmbeddings(
    model="qwen3.7-text-embedding"
)

docs_text = [
    "手机没电了，我需要充电",
    "我的手机电量耗尽，得去充电",
    "今天天气很好",
]
query_text = "手机"

# 文档用 embed_documents
doc_vecs = embedding_model.embed_documents(docs_text)

# query 用 embed_query
query_vec = embedding_model.embed_query(query_text)

print("=== 手动计算===")
for text, vec in zip(docs_text, doc_vecs):
    d = cosine_similarity(query_vec, vec)
    print(f"{text}: {d:.10f}")