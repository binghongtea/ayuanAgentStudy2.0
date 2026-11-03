from langchain_core.documents import Document

# 1.创建Document对象
doc = Document(
    page_content='这个对象是文本的内容',
    metadata={'souce':'文件来源','page':1}
)

# 2.打印Document
print(doc)
print(doc.metadata)
print(doc.page_content)