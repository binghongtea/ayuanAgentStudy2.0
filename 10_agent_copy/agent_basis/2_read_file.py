from langchain_community.chat_models import ChatTongyi
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# 1.创建模型客户端
llm = ChatOpenAI(
    model='qwen3.8-max-0902',
    base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)


# 2. 给llm添加工具
# 2.1 创建工具函数
@tool
def read_file_content(file_path:str):
    '''
    读取文本文件内容
    :param file_path:文件路径
    :return: 文件内容
    '''
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        print(f'发生错误{e}')

# 2.2 给llm绑定工具
tools = [read_file_content]
model_with_tools = llm.bind_tools(tools=tools)

# 3.调用模型

result = model_with_tools.invoke(input=r"帮我读取我本地 E:\daima\ayuanAgentStudy2.0\file\UFC.txt 的文件内容")

print(result.tool_calls)
print(type(result))


















