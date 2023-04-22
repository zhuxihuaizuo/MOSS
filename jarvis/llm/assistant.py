# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 下午2:17
# @Author  : Su Yang
# @File    : assistant.py
# @Software: PyCharm 
# @Comment : basic class of chat assistant

from abc import ABC, abstractmethod
from jarvis.memory import get_memory


class Assistant(ABC):
    def __init__(self, prompt=None, memory=get_memory(), history=None):
        if history is None:
            history = []
        self.prompt = prompt
        self.history = history  # list[dict[str, str]
        self.memory = memory

    @abstractmethod
    def generate_messages(self,
                          query: str,
                          position: str,
                          current_time: str,
                          token_limit: int) -> (list[dict[str, str]], int):
        pass

    @abstractmethod
    def create_chat_completion(self,
                               query: str,
                               position: str,
                               current_time: str,
                               temperature: float,
                               stream: bool,
                               max_tokens: int) -> str:
        pass

    def forget(self):
        self.history.clear()
