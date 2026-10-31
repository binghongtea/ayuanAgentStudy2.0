from dataclasses import dataclass, field
from typing import Any

from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import re

from .prompt import INTENT_RECOGNIZE_PROMPT


@dataclass(frozen=True)
class IntentResult:
    """
    意图识别结果：
    - intents: 意图列表
    - slots: slot 值字典
    - confidence: 置信度，0~1
    """
    intents: list[str]
    slots: dict[str, Any]
    confidence: float


class IntentRecognizer:
    """意图识别器：通过大语言模型识别用户输入的意图，输出 IntentResult。"""

    def __init__(self, llm: ChatTongyi) -> None:
        # prompt 里已包含 {history} 和 {user_input} 两个变量
        # 所以这里只需要一条 system 消息，不要再额外拼 human/ai 消息
        self.__prompt = ChatPromptTemplate.from_messages([
            ("system", INTENT_RECOGNIZE_PROMPT),
        ])
        self.__llm = llm
        self.__chain = self.__prompt | self.__llm | StrOutputParser()

    def recognize(self, user_input: str, chat_history: str | None = None) -> IntentResult:
        """
        识别用户输入的意图。
        :param user_input: 用户当前输入
        :param chat_history: 最近 N 轮会话（拼好的字符串）
        :return: IntentResult
        """
        # 1. 调用 LLM，得到 JSON 字符串
        history = chat_history or ""
        result = self.__chain.invoke(
            input={"history": history, "user_input": user_input}
        )
        # 2. 解析
        data = self.__parse_str_to_json(result)
        # 2.1 intents
        intents = data.get("intents")
        # 2.2 slots（保证 order_id / new_address 始终存在）
        slots = data.get("slots") if isinstance(data.get("slots"), dict) else {}
        # 2.3 confidence
        try:
            confidence = float(data.get("confidence"))
        except (ValueError, TypeError):
            confidence = 0.0
        confidence = max(0.0, min(1.0, confidence))
        # 3. 返回
        return IntentResult(intents, slots, confidence)

    def __parse_str_to_json(self, text: str) -> dict[str, Any]:
        """把模型输出解析为 dict，失败时返回兜底结构。"""
        fallback = {"intents": ["general"], "slots": {}, "confidence": 0.0}

        if not text or not text.strip():
            return fallback

        text = text.strip()

        # 优先直接解析
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

        # 兜底：从输出中抠出最外层 JSON（贪婪匹配，避免嵌套对象被截断）
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        return fallback