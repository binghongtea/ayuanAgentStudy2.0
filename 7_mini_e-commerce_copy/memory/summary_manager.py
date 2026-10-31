from typing import Dict, List

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .chat_history_manager import ChatHistoryManager
from .prompt import SUMMARY_GENERATION_PROMPT

# 全量存储，各对话对应各自摘要
_summary_store:Dict[str, str] = {}

# 未摘要的消息数量
_unsummarized_count:Dict[str, int] = {}

# 设置固定值
# 未摘要消息达到多少条则总结一次
SUMMARY_BATCH_SIZE = 12

class Summary:
    """
       摘要实现类
       实现：提取摘要，生成摘要
    """
    def __init__(self,session_id:str,llm:ChatOpenAI):
        self.session_id = session_id
        if self.session_id not in _summary_store:
            _summary_store[self.session_id] = ''
        self.llm = llm

    # 获取摘要
    def get_summary(self) -> str:
        return _summary_store[self.session_id]

    # 获取未摘要消息数量
    def get_unsummarized_summary(self) -> int:
        return _unsummarized_count.get(self.session_id, 0)

    # 增加未摘要消息数量 +1
    def increase_unsummarized_summary(self,delta:int = 1):
        count = _unsummarized_count.get(self.session_id, 0)
        _unsummarized_count[self.session_id] += delta

    # 判断是否到了设定的论述
    def should_summary(self) -> bool:
        return _unsummarized_count.get(self.session_id, 0) >= SUMMARY_BATCH_SIZE

    # 进行新的摘要总结，并返回新摘要，摘要主要逻辑,旧摘要 + 新对话
    def summary_generation(self, old_summary:str,unmarried_messages:List[BaseMessage]) -> str:
        if not unmarried_messages:
            return old_summary
        prompt_template = ChatPromptTemplate.from_messages([
            'system',(SUMMARY_GENERATION_PROMPT)
        ])
        chain = prompt_template | self.llm | StrOutputParser()

        #处理对话列表
        chat_history = ''
        for message in unmarried_messages:
            if isinstance(message, HumanMessage):
                chat_history += f'human:{message.content}\n'
            elif isinstance(message, AIMessage):
                chat_history += f'ai:{message.content}\n'

        result = chain.invoke(input={'old_summary': old_summary,'messages_text': unmarried_messages})

        return result.strip()


























