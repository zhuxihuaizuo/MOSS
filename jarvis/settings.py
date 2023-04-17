# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午1:58
# @Author  : Su Yang
# @File    : settings.py
# @Software: PyCharm 
# @Comment : settings

DEBUG_MODE = False

# cache
MEMORY_BACKEND = 'local'
MEMORY_INDEX = 'cache'

# proxy
PROXY_DUCKDUCKGO = True
PROXY_GOOGLE = True
PROXY_WEB_SESSION = False
PROXY_HTTP = f'http://127.0.0.1:7890'
PROXY_HTTPS = f'http://127.0.0.1:7890'

# google api
GOOGLE_API_KEY = None
CUSTOM_SEARCH_ENGINE_ID = None

# search
SEARCH_ENGINE = 'duckduckgo'
NUMBER_RESULTS = 3

# openai
OPENAI_API_KEY = None
OPENAI_API_BASE = 'https://api.openai.com/v1'
OPENAI_LLM_MODELS = ['gpt-3.5-turbo', 'gpt-4']

# llm
SMART_LLM_MODEL = 'gpt-4'
FAST_LLM_MODEL = 'gpt-3.5-turbo'
SMART_TOKEN_LIMIT = 4000
FAST_TOKEN_LIMIT = 4000
TEMPERATURE = 1
BROWSE_SUMMARY_MAX_TOKEN = 300

EMBEDDING_MODEL = ''  # TODO

# web
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

# speech
SPEECH_MODE = False
