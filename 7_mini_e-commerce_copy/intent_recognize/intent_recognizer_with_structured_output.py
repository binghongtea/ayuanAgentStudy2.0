from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from .prompt import INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT

class INTENT_RESULT(BaseModel):
    intents:list[str] = Field(description="识别出来的用户意图,可包含多个意图")
    slots:dict[str, Any]=Field(description="用户提到的订单号以及退货地址")
    confidence:float = Field(description="ai回答的置信度")

class INTENT_RECOGNIZER:
    """
        语义识别器
    """
    def __init__(self,llm:ChatOpenAI) -> None:
        # 创建提示词模板
        self.prompt_template = ChatPromptTemplate.from_messages([
            ('system',INTENT_RECOGNIZE_WITH_STRUCTURED_OUTPUT_PROMPT)
        ])
        # 创建模型客户端，并设定输出规则
        self.llm = llm.with_structured_output(INTENT_RESULT,method="function_calling")

        self.chain = self.prompt_template | self.llm

    def recognize(self,user_input:str,chat_history:str | None = None) -> INTENT_RESULT:
        # 调用大模型
        result = self.chain.invoke({'user_input':user_input,'history':chat_history})
        # 兜底
        if result is None:
            return INTENT_RESULT(intents=["general"],slots={},confidence=0.95)
        # 规范化confidence 到 0~1
        confidence = max(1.0,result['confidence'])
        return INTENT_RESULT(
            intents=result.intents,
            slots=result.slots,
            confidence=result.confidence
        )
        # result = self.chain.stream(user_input,chat_history)
        #
        # full_reply = ''
        # for chunk in result:
        #     full_reply += chunk
        #     yield chunk


