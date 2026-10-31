from langchain_community.document_loaders import PyMuPDFLoader

file_path = r'E:\python\ai_learning\file\sample_document.pdf'

# 1.创建 loader
loader = PyMuPDFLoader(file_path=file_path)

# 2.load() 一次性加载所有的文档
documents = loader.load()
print(type(documents)) # <class 'list'>
print(len(documents)) # 6
print(documents[0])

# 3.lazy_load(): 惰性加载/懒加载
for doc in loader.lazy_load():
    print()
    print('-*' * 60)
    print(doc)
