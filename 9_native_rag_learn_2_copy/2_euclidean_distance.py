from langchain_community.embeddings import DashScopeEmbeddings
import numpy as np


def l2_squared(vec1, vec2):
    """平方L2距离"""
    return float(np.sum((np.array(vec1)-np.array(vec2))**2))


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

print("=== 手动计算（平方 L2 距离，越小越相似）===")
for text, vec in zip(docs_text, doc_vecs):
    d = l2_squared(query_vec, vec)
    print(f"{text}: {d:.10f}")