# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午2:55
# @Author  : Su Yang
# @File    : embedding.py
# @Software: PyCharm 
# @Comment :

import time
from typing import Optional

import numpy as np
import openai
import paddle
from colorama import Fore
from openai.error import APIError, RateLimitError
from paddlenlp.data import JiebaTokenizer
from paddlenlp.embeddings import TokenEmbedding

import jarvis.settings as settings

paddle.device.set_device(settings.PADDLE_DEVICE)
_paddle_token_embedding: Optional[TokenEmbedding] = None
_paddle_tokenizer: Optional[JiebaTokenizer] = None
openai.api_key = settings.OPENAI_API_KEY
openai.api_base = settings.OPENAI_API_BASE


def create_embedding_aba(text) -> list:
    """Create a embedding with text-ada-002 using the OpenAI SDK"""
    num_retries = 10
    for attempt in range(num_retries):
        backoff = 2 ** (attempt + 2)
        try:
            return openai.Embedding.create(
                input=[text], model="text-embedding-ada-002"
            )["data"][0]["embedding"]
        except RateLimitError:
            pass
        except APIError as e:
            if e.http_status == 502:
                pass
            else:
                raise
            if attempt == num_retries - 1:
                raise
        if settings.DEBUG_MODE:
            print(
                Fore.RED + "Error: ",
                f"API Bad gateway. Waiting {backoff} seconds..." + Fore.RESET,
            )
        time.sleep(backoff)


def create_embedding_peddle(text: str) -> list:
    """Create a embedding with w2v using the paddle SDK
    我认为这个算法还是过分的简陋了，本地的embedding需要优化
    """
    if _paddle_token_embedding is None:
        load_paddle_embedding_model()
    # 分词
    words = _paddle_tokenizer.cut(text)
    # 获取词向量
    word_embeddings = _paddle_token_embedding.search(words)
    # 计算句向量
    sentence_embedding = np.sum(word_embeddings, axis=0) / len(words)

    return sentence_embedding


def load_paddle_embedding_model():
    """加载paddle的embedding模型，顺便初始化分句模块"""
    global _paddle_token_embedding, _paddle_tokenizer
    if _paddle_token_embedding is None:
        _paddle_token_embedding = TokenEmbedding(embedding_name="w2v.baidu_encyclopedia.target.word-word.dim300",
                                                 trainable=False)
        _paddle_tokenizer = JiebaTokenizer(vocab=_paddle_token_embedding.vocab)


def create_embedding(text: str) -> list:
    """Create a embedding with settings model"""
    if settings.EMBEDDING_BACKEND == 'openai':
        return create_embedding_aba(text)
    elif settings.EMBEDDING_BACKEND == 'paddle':
        return create_embedding_peddle(text)
    else:
        raise ValueError("Unknown EMBEDDING_BACKEND")
