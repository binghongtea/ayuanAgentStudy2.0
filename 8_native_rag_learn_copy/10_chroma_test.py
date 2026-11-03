from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document

# 1.创建 Chroma 客户端
# 第一次运行：创建新的 collection
# 第二次运行：自动加载已有的 collection
chroma_db = Chroma(
    persist_directory='./chroma_db',
    collection_name='test_collection',
    embedding_function=DashScopeEmbeddings(model='qwen3.7-text-embedding-flash')
)
# 2. 新增 document
data = [
    Document(page_content = '手机好看，但好贵'),
    Document(page_content='这手机挺漂亮，就是价格高'),
    Document(page_content='想拉屎'),
]
chroma_db.add_documents(documents=data, ids=[f"id-{i}" for i in range(1,len(data)+1)])
# 3.相似度查询
user_query = '手机不错'
result = chroma_db.similarity_search(query=user_query,k=2)
print(type(result))
print(result)

# 4.根据id进行删除
chroma_db.delete("id-1")

user_query = '手机不错'
result = chroma_db.similarity_search(query=user_query,k=2)
print(type(result))
print(result)





















