from typing import TypedDict, List, Annotated, Literal

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

from langchain_core.messages.base import BaseMessage
from langchain_core.messages import (
    SystemMessage,
    ToolMessage,
    HumanMessage,
)
from langchain_core.language_models import BaseLanguageModel
from langchain.tools import BaseTool


# ============================================================
# 1. 定义 State
# ============================================================

class ReActAgentState(TypedDict):
    # add_messages 表示：
    # 新消息不会覆盖历史消息，而是追加到历史消息中
    messages: Annotated[List[BaseMessage], add_messages]


# ============================================================
# 2. 创建 ReAct Agent
# ============================================================

def create_agent(
        model: BaseLanguageModel,
        tools: List[BaseTool],
        system_prompt: str = "你是一个有用的助手。"
):
    """
    创建一个支持 Checkpoint 的 ReAct Agent

    Args:
        model: 大语言模型实例
        tools: 工具列表
        system_prompt: 系统提示词

    Returns:
        编译完成的 LangGraph
    """

    # 绑定工具
    model_with_tools = model.bind_tools(tools)

    # 将工具转换成字典，方便通过工具名称查找
    tools_by_name = {
        tool.name: tool
        for tool in tools
    }

    # ========================================================
    # 3. 定义节点
    # ========================================================

    def llm_call(state: ReActAgentState) -> dict:
        """
        调用大模型。

        大模型会判断：
        1. 是否需要调用工具
        2. 或者直接生成最终答案
        """

        messages = [
            SystemMessage(content=system_prompt)
        ] + state["messages"]

        ai_message = model_with_tools.invoke(messages)

        # 只返回本次新增的消息
        # add_messages 会自动将它追加到历史消息中
        return {
            "messages": [ai_message]
        }

    def tool_call(state: ReActAgentState) -> dict:
        """
        执行大模型请求的工具调用
        """

        last_message = state["messages"][-1]

        tool_messages = []

        for tool_call_info in last_message.tool_calls:
            tool_name = tool_call_info["name"]
            tool_args = tool_call_info["args"]
            tool_call_id = tool_call_info["id"]

            # 查找工具
            tool = tools_by_name.get(tool_name)

            if tool is None:
                tool_result = f"工具不存在：{tool_name}"
            else:
                try:
                    tool_result = tool.invoke(tool_args)
                except Exception as e:
                    tool_result = f"工具执行失败：{str(e)}"

            # 工具执行结果必须封装成 ToolMessage
            tool_messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call_id
                )
            )

        # 一次性返回所有工具消息
        return {
            "messages": tool_messages
        }

    # ========================================================
    # 4. 定义条件路由
    # ========================================================

    def router(
            state: ReActAgentState
    ) -> Literal["tool_call", "end"]:
        """
        判断大模型是否请求调用工具
        """

        last_message = state["messages"][-1]

        if (
            hasattr(last_message, "tool_calls")
            and last_message.tool_calls
        ):
            return "tool_call"

        return "end"

    # ========================================================
    # 5. 构建图
    # ========================================================

    builder = StateGraph(ReActAgentState)

    builder.add_node("llm_call", llm_call)
    builder.add_node("tool_call", tool_call)

    builder.add_edge(START, "llm_call")

    builder.add_conditional_edges(
        "llm_call",
        router,
        {
            "tool_call": "tool_call",
            "end": END
        }
    )

    builder.add_edge("tool_call", "llm_call")

    # ========================================================
    # 6. 创建 Checkpointer
    # ========================================================

    checkpointer = InMemorySaver()

    # 编译时传入 checkpointer
    graph = builder.compile(
        checkpointer=checkpointer
    )

    return graph