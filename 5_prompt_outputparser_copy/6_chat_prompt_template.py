from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "假设你是一个{expert}专家"),
    ("human", "什么是{user_input}")
])

llm = ChatTongyi(model="qwen3-max", streaming=True)
chain = chat_prompt_template | llm

result = chain.stream(input={"expert": "AI", "user_input": "Langgraph"})
for chunk in result:
    print(chunk.content, end='', flush=True)