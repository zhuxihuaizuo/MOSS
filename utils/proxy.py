# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 下午2:07
# @Author  : Su Yang
# @File    : proxy.py
# @Software: PyCharm 
# @Comment :

def set_openai_proxy():
    import os
    from dotenv import load_dotenv
    import openai
    load_dotenv("../.env")
    openai.proxy = {
        'http': os.environ.get('PROXY_HTTP'),
        'https': os.environ.get('PROXY_HTTPS')
    }
