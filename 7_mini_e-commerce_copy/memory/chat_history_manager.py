from typing import Dict, List
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage

_session_store:Dict[str, BaseChatMessageHistory] = {}

class ChatHistoryManager:
    """
        获取历史对话
    """

    def __init__(self,session_id: str) -> None:
        self.__session_id = session_id

    def get_history(self) -> List[BaseMessage]:
        if self.__session_id not in _session_store:
            _session_store[self.__session_id] = InMemoryChatMessageHistory()
        return _session_store[self.__session_id]

    def get_messages(self,user_input:str) -> None:
        return self.get_history().messages

    def add_user_message(self,message:str | BaseMessage) -> None:
        self.get_history().add_user_message(message)

    def add_ai_message(self,message:str | BaseMessage) -> None:
        self.get_history().add_ai_message(message)

    def ger_recent_messages(self,count:int) -> List[BaseMessage]:
        messages = self.get_messages()
        return messages[-count:] if messages else []

    def clear(self) -> None:
        if self.__session_id in _session_store:
            _session_store[self.__session_id] = InMemoryChatMessageHistory()