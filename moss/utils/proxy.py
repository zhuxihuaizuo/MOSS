# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 下午2:07
# @Author  : Su Yang
# @File    : proxy.py
# @Software: PyCharm 
# @Comment :
def set_duckduckgo_proxy():
    import os
    from dotenv import load_dotenv
    from duckduckgo_search.utils import SESSION
    load_dotenv("../../.env")
    SESSION.proxies = {
        'http': os.environ.get('PROXY_HTTP'),
        'https': os.environ.get('PROXY_HTTPS')
    }


def set_openai_proxy():
    import os
    from dotenv import load_dotenv
    import openai
    load_dotenv("../../.env")
    openai.proxies = {
        'http': os.environ.get('PROXY_HTTP'),
        'https': os.environ.get('PROXY_HTTPS')
    }
