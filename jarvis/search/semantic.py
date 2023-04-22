# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 下午12:01
# @Author  : Su Yang
# @File    : semantic.py
# @Software: PyCharm 
# @Comment : semantic search functions

import re

import numpy
import paddle
from paddle.nn.functional import cosine_similarity

from jarvis.utils.embedding import create_embedding
from jarvis.utils.text import format_html_text, has_chinese
from jarvis.utils.web import *


def semantic_search_cn(result: dict, query: str, max_length: int = 800) -> str:
    """在搜索引擎结果的基础上提取中文搜索结果，并提取问题相关性较大的语句

    Args:
        result : 搜索引擎的搜索结果
        query: 搜索的问题
        max_length: 返回值的最大长度，和llm的token挂钩

    Returns:
        经过拼接的相关字符串, 如果不是中文搜索结果返回空字符串
    """

    if not has_chinese(result['title']):
        return ''
    else:
        return semantic_search_wt(result, query, max_length)


def semantic_search_en():
    pass


def semantic_search_wt(result: dict, query: str, max_length: int = 800) -> str:
    """在搜索引擎结果的基础上提取中文搜索结果，并提取问题相关性较大的语句

        Args:
            result : 搜索引擎的搜索结果
            query: 搜索的问题
            max_length: 返回值的最大长度，和llm的token挂钩

        Returns:
            经过拼接的相关字符串, 如果不是中文搜索结果返回空字符串
        """
    # TODO: 适配更多搜索引擎
    url = result.get('href')
    chunks = re.split(r'[(. )!?。！？]', format_html_text(scrape_text(url)))
    query_embedding = create_embedding(query)
    chunk_embedding_dicts = []
    for chunk in chunks:
        if len(chunk) <= 8:  # 经验值，短于这个长度的句子大多没有意义
            continue
        embedding = create_embedding(chunk)
        chunk_embedding_dicts.append({'text': chunk, 'embedding': embedding})
    texts = []
    similarity = []
    for chunk in chunk_embedding_dicts:
        cos_sim = cosine_similarity(
            paddle.to_tensor(query_embedding).unsqueeze(0),
            paddle.to_tensor(chunk['embedding']).unsqueeze(0))
        if cos_sim > 0.65:  # 经验值，大于这个值相关性较好
            texts.append(chunk['text'])
            similarity.append(cos_sim)
    # 如果句子较多去掉开头两句和结尾一句，一般都没用
    if len(texts) > 20:
        texts = texts[2:-1]
        similarity = similarity[2:-1]
    length = sum(len(text) for text in texts)
    while length > max_length:
        min_index = numpy.argmin(similarity)
        text = texts[min_index]
        del texts[min_index]
        del similarity[min_index]
        length -= len(text)
    return '。'.join(texts)
