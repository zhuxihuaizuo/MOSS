# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 下午3:05
# @Author  : Su Yang
# @File    : travel_master.py
# @Software: PyCharm 
# @Comment :
import uuid

from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.callbacks import AsyncCallbackManager
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationTokenBufferMemory
from moss.callbacks.stream_api import AsyncIteratorForApiCallbackHandler
from moss.tools.duckduckgo_search import DuckDuckGoSearchTool
# from moss.tools.sight_serach import SightSearchTool


class TravelMaster:
    def __init__(self):
        tools = [
            DuckDuckGoSearchTool(),
            # SightSearchTool()
        ]

        self.callback_manager = AsyncIteratorForApiCallbackHandler()
        llm = ChatOpenAI(streaming=True,
                         callback_manager=AsyncCallbackManager([self.callback_manager]),
                         verbose=True,
                         temperature=0.5)
        system_message = """You are a travel assistant, trying to answer all users' questions about travel"""
        agent_kwargs = {
            'system_message': system_message,
        }
        memory = ConversationTokenBufferMemory(llm=ChatOpenAI(), max_token_limit=1000,
                                               memory_key="chat_history", return_messages=True)
        self.master = initialize_agent(tools, llm,
                                       agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                       verbose=True,
                                       memory=memory,
                                       max_iterations=5,
                                       agent_kwargs=agent_kwargs)
        self.id = str(uuid.uuid4())

    async def arun(self, query: str, time: str = '', address: str = '') -> str:
        # query = f'现在的时间是：{time}\n' + f'现在的位置是：{address}\n' + query
        res = await self.master.arun(query)
        return res

    def run(self, query: str, time: str = '', address: str = '') -> str:
        # query = f'现在的时间是：{time}\n' + f'现在的位置是：{address}\n' + query
        res = self.master.run(query)
        return res

