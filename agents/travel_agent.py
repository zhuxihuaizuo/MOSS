# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 下午3:05
# @Author  : Su Yang
# @File    : travel_agent.py
# @Software: PyCharm 
# @Comment :
import time
import uuid

from langchain.agents import AgentType
from langchain.agents import initialize_agent
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationTokenBufferMemory
from callbacks.websocket_stream_conversation_agent_callback_handler import \
    WebsocketStreamConversationAgentCallbackHandler
from tools import *
from langchain.agents import ConversationalChatAgent
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate
from utils.baidu_map_api import BaiduMapApi


class TravelAgent:
    def __init__(self):
        self.baidu_map_api = BaiduMapApi()
        self.district_place_search = DistrictPlaceSearchTool()
        self.circle_place_search = CirclePlaceSearchTool()
        weather_search_tool = WeatherSearchTool()
        travel_planer = TravelPlanTool()
        tools = [
            self.district_place_search,
            self.circle_place_search,
            weather_search_tool,
            travel_planer
        ]

        # 定义输出处理
        self.callback_manager = WebsocketStreamConversationAgentCallbackHandler()
        llm = ChatOpenAI(streaming=True,
                         callback_manager=AsyncCallbackManager([self.callback_manager]),
                         verbose=True,
                         temperature=0.8,
                         max_tokens=1500)
        # 定义系统信息
        self.system_message = """你是一个旅行助手，用中文回答用户有关旅行的问题。用户问题与旅行无关时，委婉回绝。"""
        agent_kwargs = {
            'system_message': self.system_message,
        }
        # 定义记忆模块
        memory = ConversationTokenBufferMemory(llm=llm,
                                               memory_key="chat_history",
                                               return_messages=True)
        # 定义代理
        self.master = initialize_agent(tools, llm,
                                       agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                       verbose=True,
                                       memory=memory,
                                       max_iterations=2,
                                       agent_kwargs=agent_kwargs)
        # agent的唯一标识
        self.id = str(uuid.uuid4())

    async def arun(self, query: str,
                   current_time: str = time.strftime('%c'),
                   address: str = '北京',
                   location: str = '39.9096519665138,116.4041774131041') -> str:
        self.set_tool_position_info(address, location)
        self.set_time(current_time)
        res = await self.master.arun(query)
        return res

    def run(self, query: str,
            current_time: str = time.strftime('%c'),
            address: str = '北京',
            location: str = '39.9096519665138,116.4041774131041') -> str:
        self.set_tool_position_info(address, location)
        self.set_time(current_time)
        res = self.master.run(query)
        return res

    def set_time(self, current_time: str = time.strftime('%c'), address: str = '北京'):
        if isinstance(self.master.agent, ConversationalChatAgent):
            agent: ConversationalChatAgent = self.master.agent
            if isinstance(agent.llm_chain.prompt, ChatPromptTemplate):
                message = agent.llm_chain.prompt.messages[0]
                if isinstance(message, SystemMessagePromptTemplate):
                    if isinstance(message.prompt, PromptTemplate):
                        template = self.system_message + \
                                   "\n现在的用户时间是: {time}".format(time=current_time) + \
                                   "\n现在用户的地址是：{address}".format(address=address)
                        message.prompt.template = template

    def set_tool_position_info(self,
                               address: str = '北京',
                               location: str = '39.9096519665138,116.4041774131041'):
        if location == '':
            location = self.baidu_map_api.address2location(address)
        self.circle_place_search.user_location = location
