# -*- coding: utf-8 -*-
# @Time    : 2023/4/30 下午1:37
# @Author  : Su Yang
# @File    : sight_search.py
# @Software: PyCharm 
# @Comment :
from langchain.tools.base import BaseTool

from moss.utils.baidu_map_api import BaiduMapApi


class DistrictPlaceSearchTool(BaseTool):
    name = "District Place Search"
    description = (
        "当你想要获取地点列表时使用这个工具，也可以用于获取地点地址. "
        "输入是用户对于地点的要求."
    )
    region = '全国'

    def _run(self, query: str) -> str:
        """Use the tool."""
        baidu_map_api = BaiduMapApi()
        res = baidu_map_api.district_place_search(query, self.region)
        return baidu_map_api.regional_search_res2str(res)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        return self._run(query)

    def test(self, query: str):
        return self._run(query)
