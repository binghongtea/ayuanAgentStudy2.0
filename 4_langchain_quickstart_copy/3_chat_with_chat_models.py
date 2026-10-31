from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage


# 1.创建模型客户端
llm = ChatTongyi(
    model="qwen3-max"
)

# 2.准备上下文 + 当前用户消息
chat_history = [
    SystemMessage(content="背景设定：你现在是一个AI辅助老师，用来辅助 story maker 授课"),
    HumanMessage(content="你是谁？")
]

# 3.携带上下文去调用模型
result = llm.invoke(input=chat_history)

# 4.处理输出
print(type(result)) # <class 'langchain_core.messages.ai.AIMessage'>
print(result.content)
"""
content='你好！我是你的AI辅助老师，专门用来有？' 
additional_kwargs={} 
response_metadata={'model_name': 'qwen3-max', 'finish_reason': 'stop', 'request_id': 'f28c50aa-aa2f-9081-ad74-e101cae47fbb', 
'token_usage': {'input_tokens': 32, 'output_tokens': 96, 'prompt_tokens_details': 
{'cached_tokens': 0}, 'total_tokens': 128}} id='lc_run--01a0948a-5be3-7080-80fc-b38ec40fdb6e-0' 
tool_calls=[] invalid_tool_calls=[]
"""