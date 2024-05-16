#!/usr/bin/env python3
"""Cache class"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that increments the call count and calls the original method."""
        key = f"{method.__qualname__}_calls"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Decorator that stores the history of inputs and outputs for a function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that stores inputs and outputs history in Redis."""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        # Store the inputs as a string
        self._redis.rpush(input_key, str(args))
        # Execute the wrapped method and store the output
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper

class Cache:
    """the Cache class"""
    def __init__(self) -> None:
        """
        constructor:
        initialize the redis instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store data in redis
        Args:
            data: The data to be stored, which can be of type str, bytes, int, or float.

        Returns:
            The randomly generated key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: Optional[Callable[[bytes], Union[str, bytes, int, float]]] = None) -> Union[str, bytes, int, float, None]:
        """Retrieve the data from Redis using the given key and optionally convert it.

        Args:
            key: The key used to retrieve the data.
            fn: An optional callable to convert the data.

        Returns:
            The retrieved data in its original or converted format, or None if the key does not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string from Redis using the given key.

        Args:
            key: The key used to retrieve the data.

        Returns:
            The retrieved data as a string, or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer from Redis using the given key.

        Args:
            key: The key used to retrieve the data.

        Returns:
            The retrieved data as an integer, or None if the key does not exist.
        """
        return self.get(key, fn=int)
