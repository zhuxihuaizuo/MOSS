# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 上午8:22
# @Author  : Su Yang
# @File    : chatglm_6b.py
# @Software: PyCharm 
# @Comment :
from typing import Optional, List

from langchain.llms.base import LLM


# TODO：local llm
class ChatGLM6B(LLM):

    def __init__(self):
        super().__init__()

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        pass

    async def _acall(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        pass

    def _llm_type(self) -> str:
        pass
