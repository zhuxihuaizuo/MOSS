# -*- coding: utf-8 -*-
# @Time    : 2023/5/20 17:59
# @Author  : 
# @File    : websocket_stream_conversation_agent_callback_handler.py
# @Software: PyCharm 
# @Comment :
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Union, Optional
from uuid import UUID

from fastapi import WebSocket
from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema import LLMResult, BaseMessage


class WebsocketStreamConversationAgentCallbackHandler(AsyncCallbackHandler):
    """Callback handler that returns an async iterator."""

    json_str = ''
    pattern = re.compile(r'\s*\{\s*?"action":\s*"(.+?)",\s*"action_input":\s*"')
    state = 0
    action = ''
    action_input = ''
    pre_token = ''
    websocket: Optional[WebSocket] = None

    @property
    def always_verbose(self) -> bool:
        return True

    def check_websocket(self):
        """
        检查websocket是否设置
        """
        if self.websocket is None:
            raise RuntimeError('websocket未指定')

    def set_websocket(self, websocket: WebSocket):
        """
        设置websocket
        Args:
            websocket: websocket对象
        """
        self.websocket = websocket

    async def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], *, run_id: UUID,
                                  parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        self.state = 0
        self.json_str = ''
        self.action = ''
        self.action_input = ''

    async def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        # If two calls are made in a row, this resets the state
        self.check_websocket()
        self.state = 0
        self.json_str = ''
        self.action = ''
        self.action_input = ''

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        if token.endswith('\\'):
            self.pre_token = token
            return
        if self.pre_token != '':
            token = self.pre_token + token
            self.pre_token = ''
        if self.state == 0:
            # 等待action的类型
            self.json_str += token
            if "```json" in self.json_str:
                _, self.json_str = self.json_str.split("```json")
            search = self.pattern.search(self.json_str)
            if search:
                self.action = search.group(1)
                if self.action == 'Final Answer':
                    self.state = 1
                else:
                    self.state = 2
        elif self.state == 1:
            # Final Answer
            if '"' in token:
                self.state = -1
            else:
                data = {
                    'action': 'Final Answer',
                    'action_input': token
                }
                if self.websocket is not None:
                    await self.websocket.send_json(data)
                else:
                    print(token, end='')
            if self.state == -1:
                print()
        elif self.state == 2:
            # other action input
            if '"' in token:
                self.state = 3
            else:
                self.action_input += token
        elif self.state == 3:
            # sent other action message
            if self.action != 'Final Answer':
                data = {
                    'action': self.action,
                    'action_input': self.action_input
                }
                if self.websocket is not None:
                    await self.websocket.send_json(data)
                else:
                    print(data)
            self.state = -1  # 结束一轮返回

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        try:
            cleaned_output = response.generations[0][0].text.strip()
            if "```json" in cleaned_output:
                _, cleaned_output = cleaned_output.split("```json")
            if "```" in cleaned_output:
                cleaned_output, _ = cleaned_output.split("```")
            if cleaned_output.startswith("```json"):
                cleaned_output = cleaned_output[len("```json"):]
            if cleaned_output.startswith("```"):
                cleaned_output = cleaned_output[len("```"):]
            if cleaned_output.endswith("```"):
                cleaned_output = cleaned_output[: -len("```")]
            cleaned_output = cleaned_output.strip()
            response = json.loads(cleaned_output)
            action = response["action"]
            if action == 'Final Answer':
                self.websocket = None
        except Exception as e:
            print(e)

    async def on_llm_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        pass
