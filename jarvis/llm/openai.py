# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 下午3:42
# @Author  : Su Yang
# @File    : openai.py
# @Software: PyCharm 
# @Comment :
import time
from typing import Callable

import openai
from colorama import Fore
from openai.error import RateLimitError, APIError

from jarvis.llm import Assistant
from jarvis.memory import get_memory
from .utils import count_message_tokens, count_string_tokens
from jarvis import settings
from jarvis.logs import logger


class ChatGPT(Assistant):
    def __init__(self, prompt, memory=get_memory(), history=None):
        super().__init__(prompt=prompt, memory=memory, history=history)

    def generate_messages(self,
                          query: str,
                          position: str,
                          current_time: str,
                          token_limit: int = settings.GPT3_5_SETTINGS.get('token_limit')) \
            -> (list[dict[str, str]], int):
        """
        use memory and history to generate messages
        Args:
            token_limit: token limit
            query: the query string of user's request
            position: the position of the user
            current_time: the current time

        Returns:
            the context dictionary list of messages
            the current used tokens
        """
        model = settings.GPT3_5_SETTINGS.get('model')

        messages = [
            {'role': 'system', 'content': self.prompt},
            {'role': 'system', 'content': f"The current time and date is {current_time}"},
            {'role': 'system', 'content': f"The current position is {position}"},
        ]
        current_tokens_used = count_message_tokens(messages, model)

        query_tokens = count_string_tokens(query, model)
        if token_limit - current_tokens_used < query_tokens:
            raise ValueError("Token limit too small")

        # relevant_memory = (
        #     self.memory.get_relevant(query, 10)
        #     if len(self.history) == 0
        #     else self.memory.get_relevant(str(self.history[-9:]), 10)
        # )
        #
        # memory_tokens = count_string_tokens(str(relevant_memory), model)
        # while memory_tokens > (token_limit - current_tokens_used - query_tokens) << 1:
        #     relevant_memory = relevant_memory[:-1]
        #     memory_tokens = count_string_tokens(str(relevant_memory), model)
        # messages.append({
        #     'role': 'system',
        #     'content': f"This reminds you of these events from your past:\n{relevant_memory}"
        # })
        # current_tokens_used += memory_tokens

        # add history
        history = self.history
        history_tokens = count_message_tokens(history, model)
        while history_tokens > token_limit - current_tokens_used - query_tokens:
            history = history[1:]
            history_tokens = count_message_tokens(history, model)
        for h in history:
            messages.append(h)
        current_tokens_used += history_tokens

        # add query
        messages.append({'role': 'user', 'content': query})
        current_tokens_used += query_tokens

        # log
        logger.debug(f"Token limit: {token_limit}")
        logger.debug(f"Send Token Count: {current_tokens_used}")
        logger.debug(f"Tokens remaining for response: {token_limit - current_tokens_used}")
        logger.debug("------------ CONTEXT SENT TO AI ---------------")
        for message in messages:
            logger.debug(f"{message['role'].capitalize()}: {message['content']}")
        logger.debug("----------- END OF CONTEXT ----------------")

        return messages, current_tokens_used

    def create_chat_completion(self,
                               query: str,
                               position: str,
                               query_decorator: Callable[[str], str] = lambda x: x,
                               current_time: str = time.strftime('%c'),
                               temperature: float = settings.GPT3_5_SETTINGS.get('temperature'),
                               stream: bool = False,
                               max_tokens: int = 1000,
                               ) -> str:
        """
        chat with ChatGPT
        Args:
            query: the user input
            query_decorator:
            position:
            current_time:
            temperature: What sampling temperature to use, between 0 and 2.
                         Higher values like 0.8 will make the output more random,
                         while lower values like 0.2 will make it more focused and deterministic.
            stream: If set, partial message deltas will be sent, like in ChatGPT.
                    Tokens will be sent as data-only server-sent events as they become available,
                    with the stream terminated by a data: [DONE] message.
            max_tokens: The maximum number of tokens to generate in the chat completion.
                        The total length of input tokens and generated tokens is limited by the model's context length.
        Returns:

        """
        model = settings.GPT3_5_SETTINGS.get('model')
        query += f'\nAnswer in language: {settings.LANGUAGE}'
        response = None
        num_retries = 10
        if settings.DEBUG_MODE:
            print(
                Fore.GREEN
                + f"Creating chat completion with model gpt-3.5-turbo, temperature {temperature},"
                  f" max_tokens {max_tokens}" + Fore.RESET
            )
        for attempt in range(num_retries):
            backoff = 2 ** (attempt + 2)
            try:
                messages, current_token_used = self.generate_messages(query_decorator(query), position, current_time)
                remaining_token = settings.GPT3_5_SETTINGS.get('token_limit') - current_token_used
                if remaining_token - max_tokens < 0 and remaining_token > 200:
                    logger.warn('Token limit exceeded. Wrap max tokens to remaining tokens.')
                    max_tokens = remaining_token
                elif remaining_token - max_tokens < 0:
                    logger.error('Token limit exceeded.')
                    raise ValueError('Token limit exceeded')
                else:
                    logger.debug('Token limit is enough')

                openai.api_key = settings.OPENAI_API_KEY
                openai.api_base = settings.OPENAI_API_BASE
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                break
            except RateLimitError:
                if settings.DEBUG_MODE:
                    print(
                        Fore.RED + "Error: ",
                        f"Reached rate limit, passing..." + Fore.RESET,
                    )
            except APIError as e:
                if e.http_status == 502:
                    pass
                else:
                    raise
                if attempt == num_retries - 1:
                    raise
            if settings.DEBUG_MODE:
                print(
                    Fore.RED + "Error: ",
                    f"API Bad gateway. Waiting {backoff} seconds..." + Fore.RESET,
                )
            time.sleep(backoff)
        if response is None:
            raise RuntimeError(f"Failed to get response after {num_retries} retries")
        # TODO stream the response
        self.history.append({'role': 'user', 'content': query})
        self.history.append({'role': 'assistant', 'content': response.choices[0].message["content"]})
        logger.debug("Assistant response success!!!")
        return response.choices[0].message["content"]