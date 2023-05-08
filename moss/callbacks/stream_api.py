# -*- coding: utf-8 -*-
# @Time    : 2023/4/30 下午2:58
# @Author  : Su Yang
# @File    : stream_api.py
# @Software: PyCharm 
# @Comment :
from __future__ import annotations

import asyncio
import json
import re
from typing import Any, AsyncIterator, Dict, List, Literal, Union, cast

from langchain.callbacks.base import AsyncCallbackHandler
from langchain.schema import LLMResult


# TODO If used by two LLM runs in parallel this won't work as expected


class AsyncIteratorForApiCallbackHandler(AsyncCallbackHandler):
    """Callback handler that returns an async iterator."""

    queue: asyncio.Queue[str]

    done: asyncio.Event

    json_str = ''

    pattern = re.compile(r'\{\s*?"action":\s*"(.+?)",\s*"action_input":\s*"')

    state = 0

    action = ''
    action_input = ''

    @property
    def always_verbose(self) -> bool:
        return True

    def __init__(self) -> None:
        self.queue = asyncio.Queue()
        self.done = asyncio.Event()
        self.agent_done = asyncio.Event()

    async def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        # If two calls are made in a row, this resets the state
        self.done.clear()
        self.agent_done.clear()
        self.state = 0
        self.json_str = ''
        self.action = ''
        self.action_input = ''

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        # self.queue.put_nowait(token)
        if self.state == 0:
            # 等待action的类型
            self.json_str += token
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
                self.state = 3
            else:
                self.queue.put_nowait('{"action": "Final Answer", "action_input": "' + token + '"}')
        elif self.state == 2:
            # other action input
            if '"' in token:
                self.state = 3
            else:
                self.action_input += token
        elif self.state == 3:
            if self.action != 'Final Answer':
                self.queue.put_nowait('{ "action": "' + self.action + '", "action": "' + self.action_input + '"}')
            self.state = -1

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        self.done.set()
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
                self.agent_done.set()
        except Exception as e:
            print(e)

    async def on_llm_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> None:
        self.done.set()
        self.agent_done.set()

    # TODO implement the other methods

    async def aiter(self) -> AsyncIterator[str]:
        while not self.queue.empty() or not self.agent_done.is_set():
            # Wait for the next token in the queue,
            # but stop waiting if the done event is set
            done, other = await asyncio.wait(
                [
                    # NOTE: If you add other tasks here, update the code below,
                    # which assumes each set has exactly one task each
                    asyncio.ensure_future(self.queue.get()),
                    asyncio.ensure_future(self.agent_done.wait()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )

            # Cancel the other task
            other.pop().cancel()

            # Extract the value of the first completed task
            token_or_done = cast(Union[str, Literal[True]], done.pop().result())

            # If the extracted value is the boolean True, the done event was set
            if token_or_done is True:
                break

            # Otherwise, the extracted value is a token, which we yield
            yield token_or_done
