from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool

# 1.创建模型客户端
llm = ChatTongyi(
    model="qwen3-max"
)

# file_path = r"E:\python\ai_learning\file\UFC.txt"

# 2.给 LLM 添加工具
# 2.1. 创建工具
@tool(description="""
    读取文本文件内容
    :param file_path: 文本文件
    :return: 内容
""")
def read_file_content(file_path : str) -> str | None:
    try:
        # 使用 UTF-8 编码读取文件（如果遇到编码问题，可以尝试其他编码如 'gbk'）
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
            return content
    except Exception as e:
        print(f"发生错误: {e}")

# 2.2. 给 llm 绑定工具
tools = [read_file_content]
model_with_tools = llm.bind_tools(tools=tools)

# result = model_with_tools.invoke(r"读取 E:\python\ai_learning\file\UFC.txt 文件内容")
result = model_with_tools.invoke(r"你是谁？")
print(type(result))
print(result)
