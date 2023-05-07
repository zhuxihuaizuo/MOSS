# -*- coding: utf-8 -*-
# @Time    : 2023/5/4 下午6:19
# @Author  : Su Yang
# @File    : csv_embedding_beijing_sight.py
# @Software: PyCharm 
# @Comment :
# -*- coding: utf-8 -*-
# @Time    : 2023/4/26 下午6:19
# @Author  : Su Yang
# @File    : test_vectordb.py
# @Software: PyCharm
# @Comment :
import pprint

import torch
from dotenv import load_dotenv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

load_dotenv("../.env")

EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

loader = CSVLoader(file_path='../beijing_details.csv', csv_args={'delimiter': ','})

data = loader.load()

embeddings = HuggingFaceEmbeddings(model_name='GanymedeNil/text2vec-large-chinese',
                                   model_kwargs={'device': 'cpu'})

# embeddings = OpenAIEmbeddings()

faiss = FAISS.load_local("../faiss_sight_index", embeddings)

# faiss = FAISS.from_documents(data, embeddings)

query = "适合老人的景点"
docs = faiss.similarity_search(query)
pprint.pprint(docs[0])

# faiss.save_local("../faiss_sight_index")
