from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = PromptTemplate.from_template("请解释一下{concept}的概念")
model = ChatTongyi(model="qwen3-max", streaming=True)
parser = StrOutputParser()

chain = prompt | model | parser
result = chain.stream({"concept": "机器学习"})

# result 直接为字符串类型，无需再调用 .content
for chunk in result:
    print(chunk, end='', flush=True)