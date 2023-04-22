# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午1:58
# @Author  : Su Yang
# @File    : settings.py
# @Software: PyCharm 
# @Comment : settings

DEBUG_MODE = False
LANGUAGE = 'Chinese'  # us-en, zh-cn
# cache
MEMORY_BACKEND = 'local'
MEMORY_INDEX = 'cache'

# proxy
PROXY_DUCKDUCKGO = True
PROXY_GOOGLE = True
PROXY_WEB_SESSION = False
PROXY_HTTP = 'http://127.0.0.1:7890'
PROXY_HTTPS = 'http://127.0.0.1:7890'

# google api
GOOGLE_API_KEY = None
CUSTOM_SEARCH_ENGINE_ID = None

# search
SEARCH_ENGINE = 'duckduckgo'
NUMBER_RESULTS = 3

# openai
OPENAI_API_KEY = ''  # TODO push的时候记得删
OPENAI_API_BASE = 'https://api.openai-proxy.com/v1'
OPENAI_LLM_MODELS = ['gpt-3.5-turbo-0301', 'gpt-4', 'gpt-3.5-turbo']

# llm
GPT3_5_SETTINGS = {
    'model': 'gpt-3.5-turbo',
    'token_limit': 4000,
    'temperature': 1,
}

EMBEDDING_BACKEND = 'paddle'  # TODO
EMBEDDING_DIM = 300 if EMBEDDING_BACKEND == 'paddle' else 1536
PADDLE_DEVICE = 'gpu'

# web
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

# speech
SPEECH_MODE = False
