from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt_template = ChatPromptTemplate.from_messages([
    ("system", "假设你是一个电商平台的客服助手"),
    MessagesPlaceholder("history"),
    ("human", "我刚才反馈了什么问题？"),
])

chat_history = [
    ("human", "我上周买的耳机，左耳没有声音。"),
    ("ai", "非常抱歉给您带来不便，请问您是否已经尝试过重新配对或更换设备测试？")
]

llm = ChatTongyi(model="qwen3-max")
chain = chat_prompt_template | llm
result = chain.invoke(input={"history": chat_history})

print(type(result))  # <class 'langchain_core.messages.ai.AIMessage'>
print(result)        # content='你刚才反馈的是：你上周买的耳机，左耳没有声音。'
print(result.content)