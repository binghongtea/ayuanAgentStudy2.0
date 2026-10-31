from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# 1.创建 Chroma 客户端
# 第一次运行：创建新的 collection
# 第二次运行：自动加载已有的 collection
chroma_db = Chroma(
    persist_directory="./chroma_db",
    collection_name="test-collection",
    embedding_function=DashScopeEmbeddings()
)

# 2. 新增 document
data = [
    Document(page_content="手机没电了，我需要充电"),
    Document(page_content="我的手机电量耗尽，得去充电"),
    Document(page_content="今天天气很好")
]

chroma_db.add_documents(
    documents=data,
    ids=[f"id-{i}" for i in range(1, len(data) + 1)]
)

# 3.相似度查询
user_query = "手机"
result = chroma_db.similarity_search(
    query=user_query,
    k=1
)
print(result)

# 4.根据id进行删除
chroma_db.delete("id-1")
result = chroma_db.similarity_search(
    query=user_query,
    k=1
)
print(result)






















