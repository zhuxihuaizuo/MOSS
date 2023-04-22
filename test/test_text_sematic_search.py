# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 下午2:20
# @Author  : Su Yang
# @File    : test_text_sematic_search.py
# @Software: PyCharm 
# @Comment :

import json

from jarvis.search.duckduckgo import search
from jarvis.search.semantic import semantic_search_cn


def main():
    query = "什么是chatGPT"
    results = search(query, 4)
    print(results)
    results = json.loads(results)
    for result in results:
        print(semantic_search_cn(result, query))


# it seems that when cos_sim is greater than 0.65 the text is mostly similar to the question
if __name__ == '__main__':
    main()
