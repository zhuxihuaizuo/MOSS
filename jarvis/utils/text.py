# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午5:57
# @Author  : Su Yang
# @File    : text.py
# @Software: PyCharm 
# @Comment : Text processing functions
import re


def format_html_text(string: str) -> str:
    """去除字符串中不必要的成分并返回

    Args:
        string (str): 要整理的字符串

    Returns:
        str: 处理后的字符串
    """
    string = string.strip()
    text_to_replace = ("\xa0", "\u2002", "\u3000", "\u2003", '\u200b')
    for text in text_to_replace:
        string = string.replace(text, "")
    return string


def has_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    if pattern.search(text):
        return True
    else:
        return False
