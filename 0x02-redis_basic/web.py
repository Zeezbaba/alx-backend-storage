# #!/usr/bin/env python3
# """ function that uses the requests module to obtain the
# HTML content of a particular URL and returns it.
# """

# import redis
# import requests
# from typing import Callable
# from functools import wraps

# # Initialize Redis client
# r = redis.Redis()


# def track_access_count(method: Callable) -> Callable:
#     """Decorator to track the number of times a URL is accessed."""
#     @wraps(method)
#     def wrapper(url: str, *args, **kwargs):
#         count_key = f"count:{url}"
#         r.incr(count_key)
#         return method(url, *args, **kwargs)
#     return wrapper


# def cache_result(method: Callable) -> Callable:
#     """Decorator to cache the result of a URL fetch for 10 seconds."""
#     @wraps(method)
#     def wrapper(url: str, *args, **kwargs):
#         cache_key = f"cache:{url}"
#         cached_result = r.get(cache_key)
#         if cached_result:
#             return cached_result.decode('utf-8')

#         result = method(url, *args, **kwargs)
#         r.setex(cache_key, 10, result)
#         return result
#     return wrapper


# @track_access_count
# @cache_result
# def get_page(url: str) -> str:
#     """Fetch the HTML content of a particular URL."""
#     response = requests.get(url)
#     return response.text


# if __name__ == "__main__":
#     print(get_page('http://slowwly.robertomurray.co.uk'))

#!/usr/bin/env python3
"""Web caching module."""

import redis
import requests
from typing import Callable

r = redis.Redis()

def cache_request(method: Callable) -> Callable:
    """Decorator to cache a URL's HTML content for 10 seconds."""

    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"
        r.incr(count_key)

        cached = r.get(cache_key)
        if cached:
            return cached.decode('utf-8')

        html = method(url)
        r.setex(cache_key, 10, html)
        return html

    return wrapper


@cache_request
def get_page(url: str) -> str:
    """Return the content of a web page."""
    return requests.get(url).text