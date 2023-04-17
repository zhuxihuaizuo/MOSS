# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午2:29
# @Author  : Su Yang
# @File    : __init__.py.py
# @Software: PyCharm 
# @Comment :
from jarvis.memory.local import LocalMemory
from jarvis import settings


def get_memory(backend=settings.MEMORY_BACKEND, init=False):
    memory = None
    # if cfg.memory_backend == "pinecone":
    #     if not PineconeMemory:
    #         print(
    #             "Error: Pinecone is not installed. Please install pinecone"
    #             " to use Pinecone as a memory backend."
    #         )
    #     else:
    #         memory = PineconeMemory(cfg)
    #         if init:
    #             memory.clear()
    # elif cfg.memory_backend == "redis":
    #     if not RedisMemory:
    #         print(
    #             "Error: Redis is not installed. Please install redis-py to"
    #             " use Redis as a memory backend."
    #         )
    #     else:
    #         memory = RedisMemory(cfg)
    # elif cfg.memory_backend == "no_memory":
    #     memory = NoMemory(cfg)

    if memory is None:
        memory = LocalMemory()
        if init:
            memory.clear()
    return memory


__all__ = [
    "get_memory",
    "LocalMemory",
    # "RedisMemory",
    # "PineconeMemory",
    # "NoMemory",
]
