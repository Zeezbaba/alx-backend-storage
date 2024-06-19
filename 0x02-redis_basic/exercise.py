#!/usr/bin/env python3
""" a Cache class. In the __init__ method, store an instance of the
Redis client as a private variable named _redis(using redis.Redis())
and flush the instance using flushdb.
Create a store method that takes a data argument and returns a string
The method should generate a random key (e.g. using uuid),store the
input data in Redis using the random key and return the key.
Type-annotate store correctly. Remember that data can be a str, bytes,
int or float.
"""

import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        """store an instance of redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate random key and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """take string and optional callable as argument"""
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """parametrize Cache.get"""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> Optional[int]:
        """parametrize Cache.get"""
        value = self.get(key, fn=int)
        return value
