# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午8:38
# @Author  : Su Yang
# @File    : test_token_counter.py
# @Software: PyCharm 
# @Comment :
import time

from jarvis.utils.token import *


def create_chat_message(role, content):
    """
    Create a chat message with the given role and content.

    Args:
    role (str): The role of the message sender, e.g., "system", "user", or "assistant".
    content (str): The content of the message.

    Returns:
    dict: A dictionary containing the role and content of the message.
    """
    return {"role": role, "content": content}


if __name__ == '__main__':
    current_context = [
        create_chat_message("system", "what is chat GPT"),
        create_chat_message(
            "system", f"The current time and date is {time.strftime('%c')}"
        )
    ]
    print(count_message_tokens(current_context))
