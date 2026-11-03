import numpy as np
from langchain_community.embeddings import DashScopeEmbeddings


# 计算欧式距离

def euclidean_distance(vector1, vector2):
    return np.linalg.norm(np.array(vector1) - np.array(vector2))

# 创建向量模型
embedding_model = DashScopeEmbeddings(
    model='qwen3.7-text-embedding-flash'
)

# 批量处理多个文本
texts = ['手机好看，但好贵','这手机挺漂亮，就是价格高','想拉屎']

vectors = embedding_model.embed_documents(texts)

for text,vector in zip(texts,vectors):
    print(text)
    print(vector)

# 计算欧式距离
print('0和1',f'{euclidean_distance(vectors[0],vectors[1])}')
print('1和2',f'{euclidean_distance(vectors[1],vectors[2])}')
print('2和3',f'{euclidean_distance(vectors[0],vectors[2])}')
"""
0和1 0.4741971717944163
1和2 1.0871084067126597
2和3 1.0704556854390925
所以0和1更相似
"""