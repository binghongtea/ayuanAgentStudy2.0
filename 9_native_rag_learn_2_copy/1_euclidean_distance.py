import numpy as np
from langchain_community.embeddings import DashScopeEmbeddings


def euclidean_distance(a,b):
    """计算欧氏距离"""
    return np.linalg.norm(np.array(a) - np.array(b))

embedding_model = DashScopeEmbeddings(
    model="qwen3.7-text-embedding-flash"
)

# 批量处理文本列表
texts = [ "手机没电了，我需要充电",
    "我的手机电量耗尽，得去充电",
    "今天天气很好",]

results = embedding_model.embed_documents(texts)

print(f"'{texts[0]}' 与 '{texts[1]}' 的欧氏距离: {euclidean_distance(results[0], results[1])}")
print(f"'{texts[0]}' 与 '{texts[2]}' 的欧氏距离: {euclidean_distance(results[0], results[2])}")
print(f"'{texts[1]}' 与 '{texts[2]}' 的欧氏距离: {euclidean_distance(results[1], results[2])}")