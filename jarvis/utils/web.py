# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午4:23
# @Author  : Su Yang
# @File    : web.py
# @Software: PyCharm 
# @Comment : Browse a webpage and summarize it using the LLM model
from typing import List, Tuple, Union
from urllib.parse import urljoin, urlparse

import requests
from requests import Response
from bs4 import BeautifulSoup

from jarvis.memory import get_memory
from .html import extract_hyperlinks, format_hyperlinks
import jarvis.settings as settings

memory = get_memory()

session = requests.Session()
session.headers.update({"User-Agent": settings.USER_AGENT})
if settings.PROXY_WEB_SESSION:
    session.proxies = {
        'http': settings.PROXY_HTTP,
        'https': settings.PROXY_HTTPS
    }


def is_valid_url(url: str) -> bool:
    """Check if the URL is valid

    Args:
        url (str): The URL to check

    Returns:
        bool: True if the URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def sanitize_url(url: str) -> str:
    """Sanitize the URL

    Args:
        url (str): The URL to sanitize

    Returns:
        str: The sanitized URL
    """
    return urljoin(url, urlparse(url).path)


def check_local_file_access(url: str) -> bool:
    """Check if the URL is a local file

    Args:
        url (str): The URL to check

    Returns:
        bool: True if the URL is a local file, False otherwise
    """
    local_prefixes = [
        "file:///",
        "file://localhost",
        "http://localhost",
        "https://localhost",
    ]
    return any(url.startswith(prefix) for prefix in local_prefixes)


def get_response(
        url: str, timeout: int = 10
) -> Union[Tuple[None, str], Tuple[Response, None]]:
    """Get the response from a URL

    Args:
        url (str): The URL to get the response from
        timeout (int): The timeout for the HTTP request

    Returns:
        Tuple[None, str] | Tuple[Response, None]: The response and error message

    Raises:
        ValueError: If the URL is invalid
        requests.exceptions.RequestException: If the HTTP request fails
    """
    try:
        # Restrict access to local files
        if check_local_file_access(url):
            raise ValueError("Access to local files is restricted")

        # Most basic check if the URL is valid:
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError("Invalid URL format")

        sanitized_url = sanitize_url(url)

        response = session.get(sanitized_url, timeout=timeout)

        # Check if the response contains an HTTP error
        if response.status_code >= 400:
            return None, f"Error: HTTP {str(response.status_code)} error"

        return response, None
    except ValueError as ve:
        # Handle invalid URL format
        return None, f"Error: {str(ve)}"

    except requests.exceptions.RequestException as re:
        # Handle exceptions related to the HTTP request
        #  (e.g., connection errors, timeouts, etc.)
        return None, f"Error: {str(re)}"


def scrape_text(url: str) -> str:
    """Scrape text from a webpage

    Args:
        url (str): The URL to scrape text from

    Returns:
        str: The scraped text
    """
    response, error_message = get_response(url)
    if error_message:
        return error_message
    if not response:
        return "Error: Could not get response"

    soup = BeautifulSoup(response.text, "html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text


def scrape_links(url: str) -> Union[str, List[str]]:
    """Scrape links from a webpage

    Args:
        url (str): The URL to scrape links from

    Returns:
        Union[str, List[str]]: The scraped links
    """
    response, error_message = get_response(url)
    if error_message:
        return error_message
    if not response:
        return "Error: Could not get response"
    soup = BeautifulSoup(response.text, "html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    hyperlinks = extract_hyperlinks(soup, url)

    return format_hyperlinks(hyperlinks)
