# -*- coding: utf-8 -*-
# @Time    : 2023/4/27 下午3:31
# @Author  : Su Yang
# @File    : embedding.py
# @Software: PyCharm 
# @Comment :
from langchain.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain.embeddings.base import Embeddings


def get_embeddings(model: str = 'openai') -> Embeddings:
    """
    加载embedding模型
    Args:
        model: 模型的名称

    Returns:
        Embeddings
    """
    if model == "text2vec":
        print('load model text2vec-large-chinese')
        # embedding_device = "cuda" if torch.cuda.is_available() else "cpu"
        embeddings = HuggingFaceEmbeddings(model_name='GanymedeNil/text2vec-large-chinese',
                                           model_kwargs={'device': 'cpu'})
    elif model == 'openai':
        print('load model text-embedding-ada-002')
        embeddings = OpenAIEmbeddings()
    else:
        print('load model text-embedding-ada-002')
        embeddings = OpenAIEmbeddings()

    return embeddings
