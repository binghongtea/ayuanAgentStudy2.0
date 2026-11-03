from langchain_community.document_loaders import TextLoader

# 加载文本文件
file_path = r'E:\daima\ayuanAgentStudy2.0\file\中秋节.txt'

# 创建textloader
loader = TextLoader(file_path,encoding='utf-8')

# 加载文本文件
documents = loader.load()
print(documents[0].page_content)