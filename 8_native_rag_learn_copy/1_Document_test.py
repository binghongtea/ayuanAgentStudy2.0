from langchain_core.documents import Document

# 1.手动创建一个 Document 对象
document = Document(
    page_content="这个属性是文本的内容",
    metadata={"source": "文件的来源", "page": 1}
)

# 2.打印 Document 对象
print(document.page_content)
print(document.metadata)