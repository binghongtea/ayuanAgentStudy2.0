from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

# 1. 定义示例
examples = [
    {"input": "这家餐厅的服务态度特别好，菜也很好吃。", "output": "正面"},
    {"input": "等了半个小时还没上菜，太失望了。", "output": "负面"},
    {"input": "味道还行，价格也一般。", "output": "中性"}
]

# 2. 定义示例格式化模板
example_prompt = PromptTemplate.from_template(
    template="评论：{input}\n情感：{output}"
)

# 3. 创建 FewShotPromptTemplate
few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="请根据以下示例，判断用户评论的情感倾向，只需要说答案。",
    suffix="基于示例判断下面评论的情感。\n评论：{text}\n情感：",
    input_variables=["text"]
)

# 4. 调用
# prompt_text = few_shot_prompt.format(text="物流很快，包装也很用心，非常满意！")
# print(type(prompt_text))
# print(prompt_text)
# prompt_text = few_shot_prompt.invoke(input={"text": "物流很快，包装也很用心，非常满意！"})
# print(type(prompt_text)) # <class 'langchain_core.prompt_values.StringPromptValue'>
# print(prompt_text)
"""
text='请根据以下示例，判断用户评论的情感倾向，只需要说答案。\n\n
评论：这家餐厅的服务态度特别好，菜也很好吃。\n
情感：正面\n\n
评论：等了半个小时还没上菜，太失望了。\n
情感：负面\n\n
评论：味道还行，价格也一般。\n
情感：中性
\n\n基于示例判断下面评论的情感。
\n评论：物流很快，包装也很用心，非常满意！\n
情感：'

"""

llm = Tongyi(model="qwen-max")
chain = few_shot_prompt | llm
print(chain.invoke({"text": "物流很快，包装也很用心，非常满意！"}))