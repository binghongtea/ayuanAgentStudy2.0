from langchain_community.document_loaders import TextLoader

file_path = r'E:\python\ai_learning\file\中秋节.txt'

# 加载文本文件
loader = TextLoader(file_path=file_path, encoding="utf-8")

documents = loader.load()
print(len(documents))
print(documents[0].page_content)