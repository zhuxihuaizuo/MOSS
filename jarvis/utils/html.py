# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午5:30
# @Author  : Su Yang
# @File    : html.py
# @Software: PyCharm
# @Comment : HTML processing functions
from urllib.parse import urljoin
from typing import List, Tuple
from bs4 import BeautifulSoup


def extract_hyperlinks(soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str]]:
    """Extract hyperlinks from a BeautifulSoup object

    Args:
        soup (BeautifulSoup): The BeautifulSoup object
        base_url (str): The base URL

    Returns:
        List[Tuple[str, str]]: The extracted hyperlinks
    """
    return [
        (link.text, urljoin(base_url, link["href"]))
        for link in soup.find_all("a", href=True)
    ]


def format_hyperlinks(hyperlinks: List[Tuple[str, str]]) -> List[str]:
    """Format hyperlinks to be displayed to the user

    Args:
        hyperlinks (List[Tuple[str, str]]): The hyperlinks to format

    Returns:
        List[str]: The formatted hyperlinks
    """
    return [f"{link_text} ({link_url})" for link_text, link_url in hyperlinks]
