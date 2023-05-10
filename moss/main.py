# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 下午8:02
# @Author  : Su Yang
# @File    : main.py
# @Software: PyCharm 
# @Comment :
import json

from dotenv import load_dotenv

load_dotenv('../.env')

import asyncio
from master.travel_master import TravelMaster
from utils.proxy import *

set_duckduckgo_proxy()
# set_openai_proxy()

travel_master = TravelMaster()


async def output():
    async for s in travel_master.callback_manager.aiter():
        s = json.loads(s)
        if s.get('action') == 'Final Answer':
            print(s.get('action_input'), end='')
        pass


async def call(query):
    await travel_master.arun(query)


async def main():
    query = "规划在上海的详细3天游玩计划"
    print(query, end='')
    await asyncio.gather(travel_master.arun(query), output())


if __name__ == "__main__":
    asyncio.run(main())
