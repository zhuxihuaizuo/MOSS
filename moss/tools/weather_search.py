# -*- coding: utf-8 -*-
# @Time    : 2023/5/6 下午4:31
# @Author  : Su Yang
# @File    : weather_search.py
# @Software: PyCharm 
# @Comment :
from langchain.tools.base import BaseTool

from moss.utils.baidu_map_api import BaiduMapApi


class WeatherSearchTool(BaseTool):
    name = "Weather Search"
    description = (
        "当你想要获取天气信息时使用这个工具. "
        "输入是用户想要查询的地点地址，如果用户没有提供查询地址，使用用户现在的位置. "
    )

    def _run(self, query: str) -> str:
        """Use the tool."""
        baidu_map_api = BaiduMapApi()
        adcode = baidu_map_api.address2adcode(query)
        if adcode != '':
            return baidu_map_api.weather_search(adcode)
        return '抱歉，无法找到相关天气信息。'

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        return self._run(query)
