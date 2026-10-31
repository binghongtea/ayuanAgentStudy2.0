from langchain_core.documents import Document

# 1.创建 Document 对象
doc = Document(
    page_content="这个对象是文本的内容",
    metadata={"source": "文件来源", "page": 1}
)

# 2.打印 Document
print(doc.page_content) # 这个对象是文本的内容
print(doc.metadata)     # {'source': '文件来源', 'page': 1}