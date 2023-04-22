# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 上午8:08
# @Author  : Su Yang
# @File    : agent.py
# @Software: PyCharm 
# @Comment : base class of the agent class
import uuid

from jarvis.memory import get_memory, Memory


class Agent(object):
    def __init__(self,
                 ai_name: str = 'Jarvis',
                 memory: Memory = get_memory(),
                 history: list = None,
                 prompt='你是一个私人的AI助手'):
        if history is None:
            history = []
        self.ai_name = ai_name
        self.memory = memory
        self.history = history
        self.prompt = prompt
        self.id = str(uuid.uuid4())

    def clear_history(self):
        self.history.clear()
