from langchain_community.embeddings import DashScopeEmbeddings
import numpy as np

def l2_squared(vec1, vec2):
    """平方 L2 距离"""
    return float(np.sum((np.array(vec1) - np.array(vec2)) ** 2))


embedding_model = DashScopeEmbeddings(
    model="qwen3.7-text-embedding"
)

user_query = "手机"

# 批量处理多个文本
texts = ["手机没电了，我需要充电", "我的手机电量耗尽，得去充电", "今天天气很好"]
results = embedding_model.embed_documents(texts)
# results[0] results[1] results[2]

query_vec = embedding_model.embed_query(user_query)

print(f"'{texts[0]}' 与 '{user_query}' 的欧氏距离: {l2_squared(results[0], query_vec)}")
print(f"'{texts[1]}' 与 '{user_query}' 的欧氏距离: {l2_squared(results[1], query_vec)}")
print(f"'{texts[2]}' 与 '{user_query}' 的欧氏距离: {l2_squared(results[2], query_vec)}")

