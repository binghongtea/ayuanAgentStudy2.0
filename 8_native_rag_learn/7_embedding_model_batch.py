from langchain_community.embeddings import DashScopeEmbeddings

# 创建模型对象，默认使用 text-embedding-v1
embedding_model = DashScopeEmbeddings(
    model="qwen3.7-text-embedding"
)

# 批量处理多个文本
texts = ["手机没电了，我需要充电", "我的手机电量耗尽，得去充电"]
results = embedding_model.embed_documents(texts)

for text, vector in zip(texts, results):
    print(f"文本：{text}")
    print(f"向量维度：{len(vector)}")
    print(f"向量：{vector}...\n")