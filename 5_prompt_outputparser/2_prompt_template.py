from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate

# 1. 创建模型的客户端
llm = Tongyi(model="qwen-max")

# 2. 调用模型
# 2.1. 准备提示词模板
prompt_template = PromptTemplate.from_template(
    "假设你是一个{expert}，请用通俗的语言解释这段代码的作用：{content}"
)
# 2.2. 替换占位符
prompt = prompt_template.format(expert="Python 工程师", content="for i in range(3): print(i)")
print(type(prompt))  # <class 'str'>
print(prompt)
# # 2.3. 调用模型
# result = llm.stream(input=prompt)
#
# # 3. 处理输出
# for chunk in result:
#     print(chunk, end='', flush=True)