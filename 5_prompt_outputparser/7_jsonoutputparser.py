from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# 创建解析器
parser = JsonOutputParser()

# 定义提示词模板，要求模型输出JSON格式
prompt = PromptTemplate.from_template(
    "请根据以下描述，提取电影信息并以JSON格式输出。\n"
    "描述：{description}\n"
    "输出格式：{{\"title\": \"电影名\", \"director\": \"导演\", \"year\": 上映年份}}"
)

model = ChatTongyi(model="qwen3-max", streaming=True)
chain = prompt | model | parser

result = chain.invoke({"description": "《肖申克的救赎》由弗兰克·德拉邦特执导，于1994年上映。"})
print(result)       # {'title': '肖申克的救赎', 'director': '弗兰克·德拉邦特', 'year': 1994}
print(type(result)) # <class 'dict'>