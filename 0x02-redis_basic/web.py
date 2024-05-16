import redis
import requests
from functools import wraps
from typing import Callable

# Initialize Redis client
redis_client = redis.Redis()

def cache_result(expiration: int):
    """Decorator to cache the result of a function with a specified expiration time."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Check if the result is already cached
            cached_result = redis_client.get(url)
            if cached_result:
                return cached_result.decode('utf-8')

            # Get the result from the function
            result = func(url)

            # Cache the result with the specified expiration time
            redis_client.setex(url, expiration, result)
            return result
        return wrapper
    return decorator

def track_access_count(func: Callable) -> Callable:
    """Decorator to track the number of times a URL is accessed."""
    @wraps(func)
    def wrapper(url: str) -> str:
        # Increment the access count for the URL
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return func(url)
    return wrapper

@track_access_count
@cache_result(expiration=10)
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and return it.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content of the URL.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text
