from langchain_community.document_loaders import PyMuPDFLoader

file_path = r"E:\python\ai_learning\file\sample_document.pdf"

# 1.加载 PDF 文档内容
loader = PyMuPDFLoader(file_path)
docs = loader.load()
# print(type(docs)) # <class 'list'>
# print(len(docs))
# print(type(docs[0])) # <class 'langchain_core.documents.base.Document'>
# print(docs[0])
"""
page_content 每一页的内容
metadata 每一页的元信息（当前页）
"""
for idx, doc in enumerate(docs, 1):
    print(f"第{idx}页：内容如下：")
    print(doc.page_content)
    print(f"第{idx}页：元信息如下：")
    print(doc.metadata)

    print('---' * 60)
    print('\n\n')