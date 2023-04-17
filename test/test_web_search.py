# -*- coding: utf-8 -*-
# @Time    : 2023/4/17 下午9:44
# @Author  : Su Yang
# @File    : test_web_search.py
# @Software: PyCharm 
# @Comment :
import json
from pprint import pprint
from jarvis.search.duckduckgo import search
from jarvis.utils.web import *


def main():
    results = search("什么是chatGPT", 3)
    results = json.loads(results)
    for result in results:
        pprint(result['title'])
        pprint(scrape_text(result['href']))


if __name__ == "__main__":
    main()
