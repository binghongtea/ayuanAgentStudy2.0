INTENT_RECOGNIZE_PROMPT = """
你是一个电商客服场景下的意图识别器。请结合【最近 N 轮会话】和【用户当前输入】，判断用户真正想做什么，并抽取必要槽位。你只能输出一个 JSON 对象，不能输出任何解释、说明、前后缀或 Markdown 代码块。

必须遵循的 JSON 结构：
{{"intents": ["track_shipping"], "slots": {{"order_id": null, "new_address": null}}, "confidence": 0.0}}

候选 intents：
- track_shipping：物流查询
- change_address：修改收货地址
- refund：退货退款
- complaint：投诉
- general：其他/闲聊

判断规则：
- intents 可以包含一个或多个意图。
- confidence 取值 0 到 1。
- 如果用户未提到订单号，order_id 为 null；如果用户未提到新地址，new_address 为 null。
- 优先结合上下文判断；当前输入省略的信息，可以从最近会话中继承。
- 无法归入业务意图时，使用 general。

Few-shot 示例：

示例 1
【最近会话】
用户：我的订单 12345 到哪了？
客服：我帮您查一下物流。
【用户当前输入】
现在到哪了？
【输出】
{{"intents": ["track_shipping"], "slots": {{"order_id": "12345", "new_address": null}}, "confidence": 0.95}}

示例 2
【最近会话】
用户：我想把订单 88888 的收货地址改一下。
【用户当前输入】
改到北京市朝阳区幸福路 1 号。
【输出】
{{"intents": ["change_address"], "slots": {{"order_id": "88888", "new_address": "北京市朝阳区幸福路 1 号"}}, "confidence": 0.96}}

示例 3
【最近会话】
用户：这个订单我不要了。
【用户当前输入】
我要退货退款。
【输出】
{{"intents": ["refund"], "slots": {{"order_id": null, "new_address": null}}, "confidence": 0.93}}

示例 4
【最近会话】
用户：你们的客服太差了，等了一天都没人理。
【用户当前输入】
我要投诉！
【输出】
{{"intents": ["complaint"], "slots": {{"order_id": null, "new_address": null}}, "confidence": 0.94}}

示例 5
【最近会话】
用户：今天天气不错。
【用户当前输入】
适合出去走走。
【输出】
{{"intents": ["general"], "slots": {{"order_id": null, "new_address": null}}, "confidence": 0.88}}

示例 6
【最近会话】
用户：订单 66666 一直没发货，我要退款，还要改地址。
【用户当前输入】
尽快处理。
【输出】
{{"intents": ["refund", "change_address"], "slots": {{"order_id": "66666", "new_address": null}}, "confidence": 0.85}}

现在请根据以下输入进行识别：
【最近 N 轮会话】
{history}
【用户当前输入】
{user_input}
【输出】
"""


INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT = """
你是一个电商客服场景下的意图识别器。请结合【最近 N 轮会话】和【用户当前输入】，判断用户真正想做什么，并抽取必要槽位。

## 可识别的意图（intents）
- track_shipping：物流查询、订单跟踪、快递查询、查物流
- change_address：修改收货地址、更改配送地址、改地址
- refund：退货退款、申请退款、不要了
- complaint：投诉、不满、差评、服务不好
- general：一般性对话、闲聊、问候、其他无法分类的内容

## 槽位（slots）
- order_id：订单号（通常是一串数字或字母数字组合，如 06715421bjfab412）
- new_address：新的收货地址（包含省市区街道等地址信息）

## 判断规则
1. 用户询问物流、快递、发货进度 → track_shipping
2. 用户要改地址、换地址 → change_address
3. 用户要退货、退款 → refund
4. 用户表达不满、投诉 → complaint
5. 问候、闲聊、其他情况 → general
6. intents 可以包含一个或多个意图，例如同时查询物流和改地址
7. 优先结合上下文判断；当前输入省略的信息，可以从最近会话中继承
8. 用户未提到订单号，order_id 为 null；用户未提到新地址，new_address 为 null
9. 无法归入业务意图时，使用 general

## 置信度评估标准
- 0.9~1.0：意图非常明确，关键信息（如订单号、地址）完整
- 0.7~0.9：意图明确，但缺少部分关键信息
- 0.5~0.7：意图模糊，需要推测
- 0.0~0.5：无法确定意图

## 示例

示例 1
最近会话：
用户：我的订单 12345 到哪了？
客服：我帮您查一下物流。
用户当前输入：现在到哪了？
输出：intents=[track_shipping]，order_id=12345，new_address=null，confidence=0.95

示例 2
最近会话：
用户：我想把订单 88888 的收货地址改一下。
用户当前输入：改到北京市朝阳区幸福路 1 号。
输出：intents=[change_address]，order_id=88888，new_address=北京市朝阳区幸福路 1 号，confidence=0.96

示例 3
最近会话：
用户：这个订单我不要了。
用户当前输入：我要退货退款。
输出：intents=[refund]，order_id=null，new_address=null，confidence=0.93

示例 4
最近会话：
用户：你们的客服太差了，等了一天都没人理。
用户当前输入：我要投诉！
输出：intents=[complaint]，order_id=null，new_address=null，confidence=0.94

示例 5
最近会话：
用户：今天天气不错。
用户当前输入：适合出去走走。
输出：intents=[general]，order_id=null，new_address=null，confidence=0.88

示例 6
最近会话：
用户：订单 66666 一直没发货，我要退款，还要改地址。
用户当前输入：尽快处理。
输出：intents=[refund, change_address]，order_id=66666，new_address=null，confidence=0.85

现在请根据以下输入进行识别：
【最近 N 轮会话】
{history}
【用户当前输入】
{user_input}
【输出】
"""