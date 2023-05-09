# -*- coding: utf-8 -*-
# @Time    : 2023/4/29 下午4:30
# @Author  : Su Yang
# @File    : app.py
# @Software: PyCharm 
# @Comment :
import asyncio
import json

from dotenv import load_dotenv
load_dotenv('../.env')
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response, Request
from fastapi.responses import StreamingResponse
from master.travel_master import TravelMaster
from utils.proxy import *

set_duckduckgo_proxy()

app = FastAPI()

masters = {}

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(request: Request, response: Response):
    json_data = await request.json()
    chat_id = json_data.get("chat_id")
    query = json_data.get("query")
    current_time = json_data.get("current_time")
    position = json_data.get("position")
    if chat_id is None:
        data = {'error': "chat id cannot be empty"}
        response.content = json.dumps(data)
        response.status_code = 404
        return response
    if chat_id == '':
        master = TravelMaster()
        chat_id = master.id
        masters[chat_id] = master
    else:
        master = masters.get(chat_id, None)
        if master is None:
            data = {'error': "invalid chat id"}
            response.content = json.dumps(data)
            response.status_code = 404
            return response

    async def generate():
        yield json.dumps({'action': 'chat_id', 'action_input': chat_id})
        master_task = asyncio.create_task(master.arun(query, current_time, position))
        async for token in master.callback_manager.aiter():
            yield token
        await master_task

    return StreamingResponse(generate(), status_code=200, media_type='text/plain')


@app.post('/del_chat')
async def del_chat(request: Request, response: Response):
    json_data = await request.json()
    chat_id = json_data.get("chat_id")
    if chat_id is None:
        data = {'error': "chat id cannot be empty"}
        response.content = json.dumps(data)
        response.status_code = 404
        return response
    try:
        masters.pop(chat_id)
        data = {'chat_id': chat_id}
        response.content = json.dumps(data)
        response.status_code = 200
        return response
    except KeyError as error:
        data = {'error': error}
        response.content = json.dumps(data)
        response.status_code = 404
        return response


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
