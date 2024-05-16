import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts the number of times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """increments the call count and calls the original method."""
        key = f"{method.__qualname__}_calls"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """stores the history of inputs and outputs for a function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """that stores inputs and outputs history in Redis."""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        # Store the inputs as a string
        self._redis.rpush(input_key, str(args))
        # Execute the wrapped method and store the output
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result
    return wrapper


def replay(method: Callable) -> None:
    """Display the history of calls of a particular function."""
    redis_instance = method.__self__._redis
    m_name = method.__qualname__

    # Retrieve the number of calls
    call_count = int(redis_instance.get(f"{m_name}_calls") or 0)
    print(f"{m_name} was called {call_count} times:")

    # Retrieve the inputs and outputs history
    inputs = redis_instance.lrange(f"{m_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{m_name}:outputs", 0, -1)

    # Print each call's input and output
    for in_arg, out in zip(inputs, outputs):
        print(f"{m_name}(*{in_arg.decode('utf-8')}) -> {out.decode('utf-8')}")


class Cache:
    def __init__(self):
        """Initialize the Cache class with
        a Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the given data in Redis with a randomly generated key.

        Args:
            data: The data to be stored,
            which can be of type str, bytes, int, or float.

        Returns:
            The randomly generated key as a string.
        """
        # Generate a random key
        key = str(uuid.uuid4())
        # Store the data in Redis with the generated key
        self._redis.set(key, data)
        # Return the generated key
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes], Union[str, bytes, int, float]]] = None) -> Union[str, bytes, int, float, None]:
        """
        Args:
            key: The key used to retrieve the data.
            fn: An optional callable to convert the data.

        Returns:
            The retrieved data in its original or converted format,
            or None if the key does not exist.
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
            The retrieved data as an integer,
            or None if the key does not exist.
        """
        return self.get(key, fn=int)
