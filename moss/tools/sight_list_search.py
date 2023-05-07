# -*- coding: utf-8 -*-
# @Time    : 2023/4/30 下午1:37
# @Author  : Su Yang
# @File    : sight_search.py
# @Software: PyCharm 
# @Comment :
from langchain.tools.base import BaseTool

from moss.utils.baidu_map_api import district_place_search, regional_search_res2str


class SightListSearchTool(BaseTool):
    name = "Sight Search"
    description = (
        "当你想要获取景点列表时使用这个工具，也可以用于获取景点地址. "
        "输入是用户对于景点的要求，一些像[附近]的关键词不能省略."
    )
    region = '全国'

    def _run(self, query: str) -> str:
        """Use the tool."""
        res = district_place_search(query, self.region)
        return regional_search_res2str(res)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        return self._run(query)

    def test(self, query: str):
        return self._run(query)
