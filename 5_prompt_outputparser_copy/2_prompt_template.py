import os

from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

# 1.创建模型客户端
llm = Tongyi(
    model="qwen-max",
    api_key=os.environ['DASHSCOPE_API_KEY']
)

# 2. 调用模型
# 2.1. 准备提示词模板
prompt_template = PromptTemplate.from_template(
"""
请为下面这款产品写一段介绍文案：

产品：一款主打降噪和长续航的无线蓝牙耳机
目标人群：通勤上班族、学生
要求：
1. 开头一句话点明核心卖点
2. 中间分两点说明降噪和续航
3. 结尾用一句行动号召
4. 语言简洁，适合电商详情页
"""
)
# print(type(prompt_template)) # <class 'langchain_core.prompts.prompt.PromptTemplate'>
# print(prompt_template.format())

# 3. 处理输出
result = llm.stream(input=prompt_template.format())
for chunk in result:
    print(chunk, end='', flush=True)