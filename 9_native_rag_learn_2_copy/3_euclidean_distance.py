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
    collection_name="test_collection-1",
    embedding_function=embedding_model,
    collection_metadata={"hnsw:space":"l2"}
)

# 新增文档

docs =[ Document(page_content=content) for content in docs_text]

chroma_db.add_documents(documents=docs,ids=[f"id-{i}" for i in range(1,len(docs) + 1)])

# 查询
results = chroma_db.similarity_search_with_score(
    query=query_text,k=3 )

print(results)

for text,vector in zip(docs_text,results):
    print(text,vector)

for doc ,score in results:
    print(doc,score)