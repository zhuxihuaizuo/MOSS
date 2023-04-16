# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午6:49
# @Author  : Su Yang
# @File    : SearchAgent.py
# @Software: PyCharm 
# @Comment : 仅用于搜索提供AI搜索的agent

class SearchAgent:
    """
    仅用于搜索提供AI搜索的agent
    """

    def __init__(self,
                 ai_name,
                 memory):
        self.ai_name = ai_name
        self.memory = memory
        self.history = []
        self.prompt = 'You are a search agent.'

    def search(self):
        pass
