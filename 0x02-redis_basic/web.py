#!/usr/bin/env python3
""" function that uses the requests module to obtain the
HTML content of a particular URL and returns it.
"""

import redis
import requests
from typing import Callable
from functools import wraps

r = redis.Redis()


def track_access_count(method):
    """Decorator to track the number of times a URL is accessed"""
    @wraps(method)
    def wrapper(url):
        """wrapper function"""
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

            # Get new content and update cache
        key_count = "count:" + url
        html_content = method(url)

        r.incr(key_count)
        r.set(key, html_content, ex=10)
        r.expire(key, 10)
        return html_content
    return wrapper

@track_access_count
def get_page(url: str) -> str:
    """Fetch the HTML content of a particular URL"""
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
