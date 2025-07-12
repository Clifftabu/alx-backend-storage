#!/usr/bin/env python3

import redis
import requests
from typing import Callable

r = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL, caches it for 10 seconds,
    and tracks the number of times the URL was accessed.
    """
    r.incr(f"count:{url}")
    cached = r.get(url)
    if cached:
        return cached.decode('utf-8')
    response = requests.get(url)
    r.setex(url, 10, response.text)
    return response.text
