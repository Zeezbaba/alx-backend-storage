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
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """returns a Callable"""
    key = method.__qualname__
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """increment the count for the method"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """returns a callable"""
    key = method.__qualname__
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Define input and output keys based on
        the method's qualified name
        """
        input_key = f"{key}:inputs"
        output_key = f"{key}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


def replay(method: Callable) -> Callable:
    """function to display the history of
    calls of a particular function.
    """
    key = method.__qualname__

    input_key = f"{key}:inputs"
    output_key = f"{key}:outputs"

    inputs = method.__self__._redis.lrange(input_key, 0, 1)
    outputs = method.__self__._redis.lrange(output_key, 0, 1)

    print(f"{key} was called {len(inputs)} times:")
    for input_args, output in zip(inputs, outputs):
        print(f"{key}(*{input_args.decode('utf-8) -> {output.decode('utf-8")


class Cache:
    def __init__(self):
        """store an instance of redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
