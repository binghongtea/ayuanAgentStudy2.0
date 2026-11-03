from langchain_community.document_loaders import PyMuPDFLoader

# 文件位置
file_path = r'E:\daima\ayuanAgentStudy2.0\file\sample_document.pdf'

# 1. 创建loader
loader = PyMuPDFLoader(file_path = file_path)

# 2. load()一次性加载所有的文档
# documents = loader.load()
# print(type(documents))
# print(documents[0])
# print(len(documents))

# 3. laze_load() :懒加载
documents = loader.lazy_load()
for doc in documents:
    print(doc)