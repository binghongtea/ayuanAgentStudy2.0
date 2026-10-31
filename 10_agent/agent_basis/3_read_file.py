import sys

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool

# 1.创建模型客户端
llm = ChatTongyi(
    model="qwen3-max"
)

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
            return file.read()
    except Exception as e:
        print(f"发生错误: {e}")

# 2.2. 给 llm 绑定工具
tools = [read_file_content]
model_with_tools = llm.bind_tools(tools=tools)

# 3.调用模型
messages = []

user_input = r"读取 E:\python\ai_learning\file\UFC.txt 文件内容，你总结一下大概写了什么内容"
messages.append(HumanMessage(content=user_input))
result = model_with_tools.invoke(messages)
messages.append(result)

# 4. 根据 tool_calls 调用工具
tools_map = {tool.name: tool for tool in tools}
if not result.tool_calls:
    # 没有需要调用的工具，直接输出并退出
    print("没有需要调用的工具")
    print(result.content)
    sys.exit(0)

# 有 tool_calls，逐个执行
for tool_call in result.tool_calls:
    tool_name = tool_call.get("name")
    tool_args = tool_call.get("args", {})
    tool_id = tool_call.get("id")

    tool_func = tools_map.get(tool_name)

    if tool_func:
        try:
            tool_result = tool_func.invoke(tool_args)
            print(f"调用工具 '{tool_name}' 成功，结果: {tool_result}")

            # 创建 ToolMessage 并将结果添加到消息历史
            tool_message = ToolMessage(
                content=tool_result,
                tool_call_id=tool_id
            )
            messages.append(tool_message)

        except Exception as e:
            print(f"调用工具 '{tool_name}' 失败: {e}")
            tool_message = ToolMessage(
                content=f"工具调用失败: {str(e)}",
                tool_call_id=tool_id
            )
            messages.append(tool_message)
    else:
        print(f"未找到工具: {tool_name}")
        tool_message = ToolMessage(
            content=f"未找到工具: {tool_name}",
            tool_call_id=tool_id
        )
        messages.append(tool_message)

print(messages)
print("===== messages 内容 =====")
for i, msg in enumerate(messages):
    print(f"\n--- [{i}] {type(msg).__name__} ---")
    print(msg)

result = model_with_tools.invoke(messages)
print(result.content)