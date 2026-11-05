from langchain_community.embeddings import DashScopeEmbeddings
import numpy as np


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


if __name__ == '__main__':
    user_query = "Spring Boot 3.2 发布时间"

    documents = [
        "Spring Boot 3.2：2023年11月23日",
        "Spring Boot 3.1 是 Spring Boot 的重要版本，在2023年正式发布",
        "Spring Boot 3.3 是 Spring Boot 3 系列的重要版本，包含大量新功能",
        "Spring Boot 3 是 Spring 生态的新一代开发框架版本",
        "Spring Boot 的版本通常会定期更新，并提供新特性和依赖升级",
    ]

    embeddings = DashScopeEmbeddings()

    query_vector = embeddings.embed_query(user_query)
    doc_vectors = embeddings.embed_documents(documents)

    print(f"=== 查询 Q: '{user_query}' ===")
    print("-" * 80)

    for i, doc in enumerate(documents):
        sim = cosine_similarity(query_vector, doc_vectors[i])
        print(f"文档{i}: '{doc}' 相似度: {sim:.4f}")