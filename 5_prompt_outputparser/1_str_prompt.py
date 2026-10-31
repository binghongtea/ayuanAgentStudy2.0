import os

from langchain_community.llms.tongyi import Tongyi

# 1.创建模型客户端
llm = Tongyi(
    model="qwen-max",
    api_key=os.environ['DASHSCOPE_API_KEY']
)

# 2. 调用模型
# user_query_1 = "写一段耳机产品介绍"

user_query_2 = """
请为下面这款产品写一段介绍文案：

产品：一款主打降噪和长续航的无线蓝牙耳机
目标人群：通勤上班族、学生
要求：
1. 开头一句话点明核心卖点
2. 中间分两点说明降噪和续航
3. 结尾用一句行动号召
4. 语言简洁，适合电商详情页
"""

result = llm.stream(input=user_query_2)

# 3. 处理输出
for chunk in result:
    print(chunk, end='', flush=True)