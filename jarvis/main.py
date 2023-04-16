# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午2:08
# @Author  : Su Yang
# @File    : test_duckduckgo_search.py
# @Software: PyCharm 
# @Comment :

from search.duckduckgo import search
import settings


def main():
    print(search("什么是chatGPT"))


def p():
    print(settings.PROXY_HTTP)


if __name__ == "__main__":
    # main()
    print(settings.PROXY_HTTP)
    settings.PROXY_HTTP = "123"
    print(settings.PROXY_HTTP)
    print(settings.PROXY_HTTP)
    p()
