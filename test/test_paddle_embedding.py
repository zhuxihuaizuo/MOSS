# -*- coding: utf-8 -*-
# @Time    : 2023/4/17 下午6:07
# @Author  : Su Yang
# @File    : test_paddle_embedding.py
# @Software: PyCharm 
# @Comment :
import paddle
from paddlenlp.embeddings import TokenEmbedding, list_embedding_name

# paddle.device.set_device('cpu')
print(paddle.device.get_device())

token_embedding = TokenEmbedding(embedding_name="w2v.baidu_encyclopedia.target.word-word.dim300", trainable=False)
score = token_embedding.cosine_sim("你好", "再见")
print(score)
