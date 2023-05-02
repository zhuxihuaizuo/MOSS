# -*- coding: utf-8 -*-
# @Time    : 2023/5/2 上午11:55
# @Author  : Su Yang
# @File    : duckduckgo_search.py
# @Software: PyCharm 
# @Comment :
from langchain.tools import DuckDuckGoSearchRun


class DuckDuckGoSearchTool(DuckDuckGoSearchRun):
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        return self.run(query)
