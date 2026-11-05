from langchain_community.embeddings import DashScopeEmbeddings
import numpy as np

def cosine_similarity(vec1, vec2):
    """余弦相似度（值越大越相似）"""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

embedding_model = DashScopeEmbeddings(
    model="qwen3.7-text-embedding"
)

# 批量处理多个文本
texts = ["手机没电了，我需要充电", "我的手机电量耗尽，得去充电", "今天天气很好"]
results = embedding_model.embed_documents(texts)
# results[0] results[1] results[2]

print(f"'{texts[0]}' 与 '{texts[1]}' 的欧氏距离: {cosine_similarity(results[0], results[1])}")
print(f"'{texts[0]}' 与 '{texts[2]}' 的欧氏距离: {cosine_similarity(results[0], results[2])}")
print(f"'{texts[1]}' 与 '{texts[2]}' 的欧氏距离: {cosine_similarity(results[1], results[2])}")

"""
'手机没电了，我需要充电' 与 '我的手机电量耗尽，得去充电' 的欧氏距离: 0.9304346049205466
'手机没电了，我需要充电' 与 '今天天气很好' 的欧氏距离: 0.4390566919996725
'我的手机电量耗尽，得去充电' 与 '今天天气很好' 的欧氏距离: 0.45271939392009536
"""


