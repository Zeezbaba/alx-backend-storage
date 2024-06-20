#!/usr/bin/env python3
""" function that uses the requests module to obtain the
HTML content of a particular URL and returns it.
"""

import redis
import requests
from functools import wraps

r = redis.Redis()


def url_access_count(method):
    """Decorator for get_page function"""
    @wraps(method)
    def wrapper(url):
        """Wrapper function"""
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        # Get new content and update cache
        key_count = "count:" + url
        html_content = method(url)

        r.incr(key_count)
        r.setex(key, 10, html_content)
        return html_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """Obtain the HTML content of a particular URL"""
    try:
        results = requests.get(url)
        results.raise_for_status()  # Raise an HTTPError for bad responses
        return results.text
    except requests.RequestException as e:
        return f"Error: {e}"


if __name__ == "__main__":
    print(get_page('http://slowwly.robertomurray.co.uk'))
