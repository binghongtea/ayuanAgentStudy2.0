from langchain_community.embeddings import DashScopeEmbeddings
import numpy as np

def euclidean_distance(a, b):
    """计算欧氏距离"""
    return np.linalg.norm(np.array(a) - np.array(b))

if __name__ == '__main__':
    # 换一组测试文本：前两个语义相近，第三个语义无关
    texts = [
        "我喜欢的水果是苹果",
        "苹果是我最喜欢的水果",
        "今天股市大涨"
    ]

    vectors = DashScopeEmbeddings().embed_documents(texts)

    print(f"'{texts[0]}' 与 '{texts[1]}' 的欧氏距离: {euclidean_distance(vectors[0], vectors[1])}")
    print(f"'{texts[0]}' 与 '{texts[2]}' 的欧氏距离: {euclidean_distance(vectors[0], vectors[2])}")
    print(f"'{texts[1]}' 与 '{texts[2]}' 的欧氏距离: {euclidean_distance(vectors[1], vectors[2])}")