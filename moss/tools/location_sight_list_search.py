# -*- coding: utf-8 -*-
# @Time    : 2023/5/5 上午9:11
# @Author  : Su Yang
# @File    : location_sight_list_search.py
# @Software: PyCharm 
# @Comment :
from langchain.tools.base import BaseTool
from moss.utils.baidu_map_api import circle_place_search, regional_search_res2str


class LocationSightListSearchTool(BaseTool):
    name = "Location Sight Search"
    description = (
        "可以获得以用户为中心1500米以内的地点信息. "
        "输入是用户对于地点的要求."
    )
    user_location = '39.9096519665138,116.4041774131041'

    def _run(self, query: str) -> str:
        """Use the tool."""
        # 接口地址
        res = circle_place_search(query, self.user_location)
        return regional_search_res2str(res)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        return self._run(query)
