# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 下午6:12
# @Author  : Su Yang
# @File    : test_openai_api.py
# @Software: PyCharm 
# @Comment :
import openai
from jarvis import settings

openai.api_key = settings.OPENAI_API_KEY
openai.api_base = settings.OPENAI_API_BASE

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Reply in English in the following conversation"},
    {"role": "user", "content": "百度是什么"},
    {'role': "assistant", "content": "Baidu是一家中国的互联网公司，提供搜索引擎、在线广告、云存储等服务。"},
    {'role': "user", 'content': '请用英语回复我'}
]

response = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=messages,
                    temperature=0.5,
                    max_tokens=1000,
                )

print(response)
print(response.choices[0].message["content"])
# print(openai.Model.list())
