from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


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

# 创建 Chroma 客户端（l2 = 平方欧氏距离）
chroma_db = Chroma(
    persist_directory="./chroma_db",
    collection_name="test-collection-1",
    embedding_function=embedding_model,
    collection_metadata={"hnsw:space": "l2"},
)

# 新增文档
data = [Document(page_content=t) for t in docs_text]
chroma_db.add_documents(
    documents=data,
    ids=[f"id-{i}" for i in range(1, len(data) + 1)],
)

# 查询（Chroma 内部对 query 调用 embed_query）
print("=== Chroma similarity_search_with_score（越小越相似）===")
results = chroma_db.similarity_search_with_score(query_text, k=3)
print(results)

"""
[
(Document(metadata={}, page_content='手机没电了，我需要充电'), 0.7439055351478441), 
(Document(metadata={}, page_content='我的手机电量耗尽，得去充电'), 0.8034819136816602), 
(Document(metadata={}, page_content='今天天气很好'), 1.1656645428958228)
]
"""