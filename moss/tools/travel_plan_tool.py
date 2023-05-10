# -*- coding: utf-8 -*-
# @Time    : 2023/5/9 21:52
# @Author  : 
# @File    : travel_plan_tool.py
# @Software: PyCharm 
# @Comment :
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.tools.base import BaseTool


class TravelPlanTool(BaseTool):
    name = "Travel Plan Generator"
    description = (
        "当你想生成旅行计划时使用这个工具。"
        """输入用户的需求"""
    )

    def _run(self, query: str) -> str:
        """Use the tool."""
        chat = ChatOpenAI(temperature=0.8, max_tokens=1000)
        res = chat([HumanMessage(content=f'生成一个详细的旅行计划，需求如下：{query}')])
        return res.content

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        return self._run(query)
