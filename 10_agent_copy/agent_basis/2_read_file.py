from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool

# 1.创建模型客户端
llm = ChatTongyi(
    model="qwen3-max"
)

# 2.给 LLM 添加工具
# 2.1. 创建工具
@tool
# Function must have a docstring if description not provided.
def read_file_content(file_path: str) -> str | None:
    """
    读取文件内容
    :param file_path: 文档路径
    :return: 文档内容
    """
    try:
        # 使用 UTF-8 编码读取文件（如果遇到编码问题，可以尝试其他编码如 'gbk'）
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        print(f"发生错误: {e}")

# 2.2. 给 llm 绑定工具
tools = [read_file_content]
model_with_tools = llm.bind_tools(tools=tools)

# 3. 调用模型
# result = model_with_tools.invoke(r"帮我读取我本地的 E:\python\ai_learning\file\UFC.txt 文件内容")
result = model_with_tools.invoke(r"你是谁？")
print(type(result)) # <class 'langchain_core.messages.ai.AIMessage'>
print(result)
"""
content='' 
additional_kwargs={'tool_calls': [{'function': {'arguments': '{"file_path": "E:\\\\python\\\\ai_learning\\\\file\\\\UFC.txt"}', 'name': 'read_file_content'}, 
'id': 'call_ff8e53fd23dc401893e16e31', 'index': 0, 'type': 'function'}]} response_metadata={'model_name': 'q
wen3-max', 'finish_reason': 'tool_calls', 'request_id': 'efa8cfe5-dac4-9066-9b6a-f51ca841f97a', 'token_usage': {'input_tokens': 292, 'output_tokens': 33, 'prompt_tokens_details': {'cached_tokens': 256}, 'total_tokens': 325}} id='lc_run--01a1018b-52ff-7f40-b915-1cb655e92138-0' tool_calls=[{'name': 'read_file_content', 'args': {'file_path': 'E:\\python\\ai_learning\\file\\UFC.txt'}, 'id': 'call_ff8e53fd23dc401893e16e31', 'type': 'tool_call'}] invalid_tool_calls=[]

"""




















