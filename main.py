# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 下午8:02
# @Author  : Su Yang
# @File    : main.py
# @Software: PyCharm 
# @Comment :

from dotenv import load_dotenv

load_dotenv('.env')

import asyncio
from agents import TravelAgent

travel_master = TravelAgent()


async def call(query):
    await travel_master.arun(query)


async def main():
    query = "天安门附近的饭店"
    print(query, end='')
    await asyncio.gather(travel_master.arun(query))


if __name__ == "__main__":
    asyncio.run(main())
