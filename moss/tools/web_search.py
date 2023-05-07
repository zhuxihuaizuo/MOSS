# -*- coding: utf-8 -*-
# @Time    : 2023/5/2 上午11:55
# @Author  : Su Yang
# @File    : web_search.py
# @Software: PyCharm 
# @Comment :
from typing import Optional

from langchain.callbacks.manager import AsyncCallbackManagerForToolRun
from langchain.tools import DuckDuckGoSearchRun


class WebSearchTool(DuckDuckGoSearchRun):
    name = "Web Search"
    description = (
        "当你需要回答关于最近发生的事件的问题时可以使用这工具. "
        "当需要对景点进行介绍时也可以使用这个工具. "
        "输入是要搜索的内容."
    )

    def __init__(self):
        super().__init__()
        self.api_wrapper.region = 'cn-zh'

    async def _arun(self,
                    query: str,
                    run_manager: Optional[AsyncCallbackManagerForToolRun] = None, ) -> str:
        """Use the tool asynchronously."""
        return self.run(query)
