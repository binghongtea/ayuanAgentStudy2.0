from typing import TypedDict
from typing_extensions import NotRequired

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command

class State(TypedDict):
    amount: int
    approved: NotRequired[bool]

def apply_refund(state: State):
    print(f"准备退款：{state['amount']} 元")
    return state

def human_review(state: State):
    print(f"before: 人工审批 {state}")
    # ✅ 启用 interrupt：图会在这里暂停，等待 Command(resume=...)
    approved = interrupt({
        "message": "退款金额较大，请人工审批",
        "amount": state["amount"]
    })
    print(f"after: 人工审批 {approved} {state}")
    state["approved"] = approved
    return state

def execute_refund(state: State):
    if state["approved"]:
        print("审批通过，执行退款")
        print(f"成功退款：{state['amount']} 元")
    else:
        print("审批拒绝，不执行退款")
    return state

builder = StateGraph(State)
builder.add_node("apply_refund", apply_refund)
builder.add_node("human_review", human_review)
builder.add_node("execute_refund", execute_refund)

builder.add_edge(START, "apply_refund")
builder.add_edge("apply_refund", "human_review")
builder.add_edge("human_review", "execute_refund")
builder.add_edge("execute_refund", END)

from json_file_saver import JsonFileSaver
checkpointer = JsonFileSaver("checkpoint.json")
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "refund-001"}}

# ✅ 第一次执行：触发 interrupt，图暂停
graph.invoke({"amount": 5000}, config=config)

# 查看状态（应能看到 __interrupt__）
for idx, snapshot in enumerate(graph.get_state_history(config)):
    print(idx, snapshot)

# print("\n请选择：")
# print("1. 同意退款")
# print("2. 拒绝退款")
#
# while True:
#     choice = input("\n请输入 1 或 2：").strip()
#     if choice == "1":
#         approved = True
#         print("\n人工操作：同意退款")
#         break
#     elif choice == "2":
#         approved = False
#         print("\n人工操作：拒绝退款")
#         break
#     else:
#         print("输入错误，请输入 1 或 2")
#
# # ✅ 恢复：从 interrupt 处继续，apply_refund 不会重跑
# result = graph.invoke(Command(resume=approved), config=config)
#
# print("\n==============================")
# print("          最终结果")
# print("==============================")
# print(result)
# print("长度", len(list(graph.get_state_history(config))))
# for idx, snapshot in enumerate(graph.get_state_history(config)):
#     print(idx, snapshot)