# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午6:49
# @Author  : Su Yang
# @File    : search_agent.py
# @Software: PyCharm 
# @Comment : 仅用于提供网页AI搜索的agent
import json
import time

import jarvis.settings as settings
from jarvis.agent.agent import Agent
from jarvis.llm import ChatGPT
from jarvis.memory import get_memory, Memory
from jarvis.search import search


class SearchAgent(Agent):
    """
    仅用于搜索提供AI搜索的agent
    """

    def __init__(self, ai_name: str = 'Jarvis', memory: Memory = get_memory()):
        super().__init__(ai_name, memory, [], '你是一个AI助手')
        self.assistant = ChatGPT(self.prompt, history=[])
        self.search_result = ''

    def search(self, query: str,
               num_results: int = settings.NUMBER_RESULTS,
               current_time=time.strftime('%c'),
               position='') -> str:
        results = search(query, num_results)
        results = json.loads(results)
        self.search_result = ''
        for result in results:
            text = result['body']
            self.search_result += text

        assistant_reply = self.assistant.create_chat_completion(
            query=query,
            position=position,
            current_time=current_time,
            temperature=1,
            stream=False,
            max_tokens=1000,
            query_decorator=self.query_decorator
        )

        return assistant_reply

    def query_decorator(self, query: str) -> str:
        return f"""Web search result:
{self.search_result}
Instructions: Using the knowledge you have learned and the provided web search results, write a comprehensive reply to the given query.
If the provided search results refer to multiple subjects with the same name, write separate answers for each subject.
If the web search result is insufficient, using the knowledge you have learned write a reply to the given query.
Query: {query}"""
