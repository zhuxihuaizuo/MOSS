# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午6:49
# @Author  : Su Yang
# @File    : search_agent.py
# @Software: PyCharm 
# @Comment : 仅用于提供网页AI搜索的agent
import json

import jarvis.settings as settings
from jarvis.chat import chat_with_ai
from jarvis.search import search
from jarvis.utils.web import scrape_text
from jarvis.memory.memory import Memory


class SearchAgent:
    """
    仅用于搜索提供AI搜索的agent
    """

    def __init__(self,
                 ai_name,
                 memory: Memory):
        self.ai_name = ai_name
        self.memory = memory
        self.history = []
        self.prompt = 'You are a search engine.'

    def search(self, query: str, num_results: int = settings.NUMBER_RESULTS):
        results = search(query, num_results)
        results = json.loads(results)
        for result in results:
            text = scrape_text(result['href'])  # TODO 适应不同的搜索引擎
            memory_to_add = (
                f"query: {result['href']} "
                f"\nResult: {text} "
            )
            self.memory.add(memory_to_add)

        assistant_reply = chat_with_ai(
            self.prompt,
            query,
            self.history,
            self.memory,
            settings.FAST_TOKEN_LIMIT,
        )
        return assistant_reply

    def clear_history(self):
        self.history.clear()
