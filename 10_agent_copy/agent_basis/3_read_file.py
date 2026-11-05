import sys

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# 1.创建模型客户端
llm = ChatOpenAI(
    model='qwen3.8-max-0902',
    base_url="https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 2.给 LLM 添加工具
# 2.1. 创建工具
@tool
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
messages = []
user_input = r"帮我读取我本地 E:\daima\ayuanAgentStudy2.0\file\UFC.txt 的文件内容"
messages.append(HumanMessage(content=user_input))

result = model_with_tools.invoke(input=messages)
messages.append(result)

# 4.根据 tool_calls调用工具
tools_map = {t.name : t for t in tools}

if not result.tool_calls:
    # 没有需要调用的工具，直接输出并退出
    print('没有需要调用的工具')
    print(result.content)
    sys.exit(0)

# 有tool_calls,逐个执行
for tool_call in result.tool_calls:
    tool_name = tool_call.get('name')
    tool_args = tool_call.get('args',{})
    tool_id = tool_call.get('id')

    tool_func = tools_map.get(tool_name)

    if tool_func:
        try:
            tool_result = tool_func.invoke(tool_args)
            print(f"调用工具‘{tool_name}’成功，结果是{tool_result}")

            # 创建 ToolMessage 并将结果添加到消息历史
            tool_message = ToolMessage(
                content=tool_result,
                tool_call_id = tool_id,
            )
            messages.append(tool_message)
        except Exception as e:
            print(f"调用工具‘{tool_name}’失败{e}")
            tool_message = ToolMessage(
                content=f'调用工具‘{tool_name}’失败{str(e)}',
                tool_call_id = tool_id,
            )
            messages.append(tool_message)
    else :
        print(f"未找到{tool_name}工具")
        tool_message = ToolMessage(
            content=f'未找到{tool_name}工具',
            tool_call_id=tool_id,
        )
        messages.append(tool_message)

print(messages)
result = model_with_tools.invoke(input=messages)
print(result)




























