from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser


# 定义提示词模板，要求模型输出JSON格式
prompt = PromptTemplate.from_template(
    "请根据以下描述，提取电影信息并输出。\n"
    "描述：{description}\n"
    "输出格式：电影名称，名称"
)

model = ChatTongyi(model="qwen3-max", streaming=True)
parser = JsonOutputParser()
chain = prompt | model | parser

result = chain.invoke({"description": "《肖申克的救赎》由弗兰克·德拉邦特执导，于1994年上映。"})
print(type(result))
print(result)