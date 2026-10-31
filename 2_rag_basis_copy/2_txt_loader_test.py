from langchain_community.document_loaders import TextLoader

file_path = r'E:\python\ai_learning\file\UFC.txt'
# 1.加载 txt 文档
docs = TextLoader(file_path, encoding="utf-8").load()
print(type(docs)) # <class 'list'>
print(len(docs))
print(docs[0])