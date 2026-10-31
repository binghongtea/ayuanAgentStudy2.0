from langchain_community.document_loaders import PyMuPDFLoader

file_path = r"/file/sample_document.pdf"

# 1.获取 PDF 文档内容
docs = PyMuPDFLoader(file_path).load()
print(type(docs)) # <class 'list'>
print(f"列表长度：{len(docs)}") # 6
print(type(docs[0])) # <class 'langchain_core.documents.base.Document'>
# print(docs[0])


# 2. 打印 PDF 文档内容
for idx, doc in enumerate(docs, 1):
    print(f"第{idx}页：内容如下：")
    print(doc.page_content)
    print(f"第{idx}页：元信息如下：")
    print(doc.metadata)

    print('---' * 60)
    print('\n\n')