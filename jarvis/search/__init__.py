# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午1:52
# @Author  : Su Yang
# @File    : __init__.py.py
# @Software: PyCharm 
# @Comment :
from jarvis import settings
from .semantic import semantic_search_cn


def search(query: str, num_results: int = 8) -> str:
    """Return the results of a search
    Args:
        query (str): The search query.
        num_results (int): The number of results to return.
    Returns:
        str: The results of the search.
    """
    if settings.SEARCH_ENGINE == 'duckduckgo':
        from .duckduckgo import search
        return search(query, num_results)
    elif settings.SEARCH_ENGINE == 'google':
        from .google import search
        return search(query, num_results)
    else:
        raise ValueError("Unknown search engine")
