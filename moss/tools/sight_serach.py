# -*- coding: utf-8 -*-
# @Time    : 2023/4/30 下午1:37
# @Author  : Su Yang
# @File    : sight_search.py
# @Software: PyCharm 
# @Comment :
from langchain import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models import ChatOpenAI

from moss.utils.embedding import get_embeddings

from pydantic import Field

from langchain.tools.base import BaseTool
from langchain.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper

embeddings = get_embeddings('openai')
faiss = FAISS.load_local("../faiss_sight_index", embeddings)
chat = ChatOpenAI(temperature=0)
sight_search = RetrievalQAWithSourcesChain.from_chain_type(chat, chain_type="stuff",
                                                           retriever=faiss.as_retriever(),
                                                           reduce_k_below_max_tokens=True,
                                                           max_tokens_limit=2000)


class SightSearchTool(BaseTool):
    name = "Sight Search"
    description = (
        "Useful for when you need to recommend sight. "
        "Input should be user's requirements."
    )
    api_wrapper: DuckDuckGoSearchAPIWrapper = Field(
        default_factory=DuckDuckGoSearchAPIWrapper
    )

    def _run(self, query: str) -> str:
        """Use the tool."""
        return sight_search({"question": f"{query}"}, return_only_outputs=True).get('answer', '')

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        return self._run(query)
