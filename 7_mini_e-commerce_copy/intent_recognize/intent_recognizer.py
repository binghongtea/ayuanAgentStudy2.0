import json
import re
from typing import Any
from dataclasses import dataclass


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from intent_recognize.prompt import INTENT_RECOGNIZE_PROMPT


@dataclass(frozen=True)
class IntentResult:
    intents:list[str]
    slots: dict[str, Any]
    confidence: float

class IntentRecognizer:

    def __init__(self,llm:ChatOpenAI) -> None:
        self.__prompt = ChatPromptTemplate.from_messages([
            ('system',INTENT_RECOGNIZE_PROMPT)
        ])

        self.__llm = llm
        self.__chain = self.__prompt | self.__llm | StrOutputParser()

    def recognize(self,user_input:str,chat_history:str | None = None) -> IntentResult:
        # 1.调用llm，得到json字符串
        history = chat_history or ""
        result = self.__chain.invoke({'user_input':user_input,'history':history})

        # 2. 解析
        data = self.__parse_str_to_json(result)
        # 2.1 intents
        intents = data.get("intents")
        if isinstance(intents, str):
            intents = [intents]
        intents = [intent for intent in intents if isinstance(intent, str) and intent.strip()] if isinstance(intents, list) else []
        intents = intents or ["general"]
        # 2.2 slots（保证 order_id / new_address 始终存在）
        slots = data.get("slots") if isinstance(data.get("slots"), dict) else {}
        slots = {"order_id": None, "new_address": None, **slots}
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
