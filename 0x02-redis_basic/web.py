#!/usr/bin/env python3

import redis
import requests

r = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL, cache it for 10 seconds,
    and track the number of times the URL was accessed in Redis.
    """
    r.incr(f"count:{url}")
    cached_page = r.get(url)
    if cached_page:
        return cached_page.decode('utf-8')
    response = requests.get(url)
    r.setex(url, 10, response.text)
    return response.text
