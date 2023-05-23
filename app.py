# -*- coding: utf-8 -*-
# @Time    : 2023/4/29 下午4:30
# @Author  : Su Yang
# @File    : app.py
# @Software: PyCharm 
# @Comment :
import asyncio
import json

from dotenv import load_dotenv

load_dotenv('.env')
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response, Request, WebSocket
from agents.travel_agent import TravelAgent

app = FastAPI()

# 存储agent对象
agents = {}

# 跨域
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


@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    json_data = await websocket.receive_json()
    chat_id = json_data.get("chat_id")
    query = json_data.get("query")
    # current_time = json_data.get("current_time")
    position = json_data.get("position")
    if chat_id is None:
        data = {'error': "chat id cannot be empty"}
        await websocket.send_json(data=data)
        return
    if chat_id == '':
        # TODO 支持更多agent
        master = TravelAgent()
        chat_id = master.id
        agents[chat_id] = master
    else:
        master = agents.get(chat_id, None)
        if master is None:
            data = {'error': "invalid chat id"}
            await websocket.send_json(data=data)
            return

    await websocket.send_json({'action': 'chat_id', 'action_input': chat_id})
    master.callback_manager.set_websocket(websocket)
    master_task = asyncio.create_task(master.arun(query, address=position))
    await master_task


@app.delete('/chat')
async def chat(request: Request, response: Response):
    json_data = await request.json()
    chat_id = json_data.get("chat_id")
    if chat_id is None:
        data = {'error': "chat id cannot be empty"}
        response.content = json.dumps(data)
        response.status_code = 404
        return response
    try:
        agents.pop(chat_id)
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
