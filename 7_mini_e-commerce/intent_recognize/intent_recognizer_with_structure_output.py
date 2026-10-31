from typing import Any

from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from .prompt import INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT

class IntentResult(BaseModel):
    """意图识别结果：通过大语言模型识别用户输入的意图，输出结构化数据。"""
    intents: list[str] = Field(description="意图列表，每个元素为一个意图名称")
    slots: dict[str, Any] = Field(description="slot值字典，键为slot名称，值为slot值")
    confidence: float = Field(description="置信度分数，取值范围0~1，越大表示越确信该意图")


class IntentRecognizer:
    """
    意图识别器：通过大语言模型识别用户输入的意图，输出 IntentResult 对象
    """

    def __init__(self, llm: ChatTongyi) -> None:
        """
        初始化意图识别
        :param llm: 大语言模型
        """
        self.__prompt = ChatPromptTemplate.from_messages([
            ("system", INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT),
        ])
        self.__structured_llm = llm.with_structured_output(IntentResult)
        self.__chain = self.__prompt | self.__structured_llm

    def recognize(self, user_input: str, chat_history: str | None = None) -> IntentResult:
        """
        识别用户输入的意图
        :param user_input: 用户当前输入
        :param chat_history: 最近 N 轮会话
        :return: 意图识别结果
        """
        # 1. 调用 LLM
        result = self.__chain.invoke(
            input={"history": chat_history or "", "user_input": user_input}
        )

        # 2. 兜底
        if result is None:
            return IntentResult(intents=["general"], slots={}, confidence=0.0)

        # 3. 规范化 confidence 到 0~1
        confidence = max(0.0, min(1.0, result.confidence))

        return IntentResult(
            intents=result.intents,
            slots=result.slots,
            confidence=confidence
        )