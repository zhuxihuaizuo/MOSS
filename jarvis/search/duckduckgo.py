# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午1:53
# @Author  : Su Yang
# @File    : duckduckgo.py
# @Software: PyCharm 
# @Comment : duckduckgo search
import json

from duckduckgo_search import ddg
from duckduckgo_search.utils import SESSION
import jarvis.settings as settings


def search(query: str, num_results: int = 8) -> str:
    """Return the results of a google search
    Args:
        query (str): The search query.
        num_results (int): The number of results to return.
    Returns:
        str: The results of the search.
    """
    if settings.PROXY_DUCKDUCKGO:
        SESSION.proxies = {
            'http': settings.PROXY_HTTP,
            'https': settings.PROXY_HTTPS
        }

    search_results = []
    if not query:
        return json.dumps(search_results)

    results = ddg(query, region=settings.LANGUAGE, max_results=num_results)
    if not results:
        return json.dumps(search_results)

    for j in results:
        search_results.append(j)
    # return format [{'title': '', 'href': href, 'body': body}, ...]
    return json.dumps(search_results, ensure_ascii=False, indent=4)
