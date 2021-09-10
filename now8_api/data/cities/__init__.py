"""Module to store the common classes and functions for all APIs."""

import requests  # type: ignore
from pydantic import HttpUrl


async def get_json(url: HttpUrl) -> dict:
    """Fetch the given URL and returns the result as a dictionary.

     Arguments:
        url: URL to fetch.

    Returns:
        List of dictionaries with the parsed answer.
    """
    request = requests.get(url)
    request.raise_for_status()
    return request.json()
