# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午2:08
# @Author  : Su Yang
# @File    : test_duckduckgo_search.py
# @Software: PyCharm 
# @Comment :

from agent.search_agent import SearchAgent


def search_service():
    search_agent = SearchAgent()
    relpy = search_agent.search('流浪地球2')
    print(relpy)


if __name__ == "__main__":
    search_service()
