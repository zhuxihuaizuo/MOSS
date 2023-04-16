# -*- coding: utf-8 -*-
# @Time    : 2023/4/16 下午1:53
# @Author  : Su Yang
# @File    : google.py
# @Software: PyCharm 
# @Comment :
import json
from typing import List, Union
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import jarvis.settings as settings


def search(query: str, num_results: int = 8) -> Union[str, List[str]]:
    """Return the results of a google search using the official Google API
    Args:
        query (str): The search query.
        num_results (int): The number of results to return.
    Returns:
        str: The results of the search.
    """

    try:
        # Get the Google API key and Custom Search Engine ID from the config file
        api_key = settings.GOOGLE_API_KEY
        custom_search_engine_id = settings.CUSTOM_SEARCH_ENGINE_ID

        # Initialize the Custom Search API service
        service = build("customsearch", "v1", developerKey=api_key)

        # Send the search query and retrieve the results
        result = (
            service.cse()
            .list(q=query, cx=custom_search_engine_id, num=num_results)
            .execute()
        )

        # Extract the search result items from the response
        search_results = result.get("items", [])

        # Create a list of only the URLs from the search results
        search_results_links = [item["link"] for item in search_results]

    except HttpError as e:
        # Handle errors in the API call
        error_details = json.loads(e.content.decode())

        # Check if the error is related to an invalid or missing API key
        if error_details.get("error", {}).get(
                "code"
        ) == 403 and "invalid API key" in error_details.get("error", {}).get(
            "message", ""
        ):
            return "Error: The provided Google API key is invalid or missing."
        else:
            return f"Error: {e}"

    # Return the list of search result URLs
    return search_results_links
