from langchain_community.document_loaders import TextLoader

file_path = r"E:\python\ai_learning\file\UFC.txt"
# 1.获取TXT文档内容
docs = TextLoader(file_path, encoding="utf-8").load()
print(docs) # [Document()]

# 2. 打印 txt 文档内容
print(docs[0].page_content)
