from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = r'E:\python\ai_learning\file\历史文化.txt'

# 1.加载文档
loader = TextLoader(file_path=file_path, encoding='utf-8')
docs = loader.load()
print(len(docs)) # 1

# 2.创建 RecursiveCharacterTextSplitter 对象
splitter = RecursiveCharacterTextSplitter(
    chunk_size=60,
    chunk_overlap=8,
    separators=["\n\n", "\n", "。", "，", "、", " ", ""],
    length_function=len
)

# 3.文本拆分
chunks = splitter.split_text(docs[0].page_content)
for i, chunk in enumerate(chunks ,1):
    print(f"--- 块 {i} (长度: {len(chunk)}) ---")
    print(chunk)
    print()