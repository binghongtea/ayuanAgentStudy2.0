from langchain_community.embeddings import DashScopeEmbeddings
import numpy as np

def euclidean_distance(a, b):
    """计算距离"""
    return np.linalg.norm(np.array(a) - np.array(b))

# 创建模型对象，默认使用 text-embedding-v1
embedding_model = DashScopeEmbeddings(
    model="qwen3.7-text-embedding"
)

# 批量处理多个文本
texts = ["手机没电了，我需要充电", "我的手机电量耗尽，得去充电", "今天天气很好"]
# results[0] results[1] results[2]
results = embedding_model.embed_documents(texts)

print(f"'{texts[0]}' 与 '{texts[1]}' 的欧氏距离: {euclidean_distance(results[0], results[1])}")
print(f"'{texts[0]}' 与 '{texts[2]}' 的欧氏距离: {euclidean_distance(results[0], results[2])}")
print(f"'{texts[1]}' 与 '{texts[2]}' 的欧氏距离: {euclidean_distance(results[1], results[2])}")