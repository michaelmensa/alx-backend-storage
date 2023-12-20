import requests
from functools import wraps
from typing import Any, Callable
import redis


# Connect to a local Redis server
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def cache_page(expiration=10) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            url = args[0]  # Assuming the URL is the first argument

            # Check if the result is in the Redis cache
            cached_result = redis_client.get(f'page:{url}')
            if cached_result is not None:
                count_key = f'count:{url}'
                count = redis_client.get(count_key) or 0
                count = int(count) + 1
                redis_client.set(count_key, count, ex=expiration)
                return cached_result.decode('utf-8')

            # If not cached, fetch the page content
            result = func(*args, **kwargs)

            # Cache the result in Redis with the specified expiration time
            redis_client.set(f'page:{url}', result, ex=expiration)

            # Increment the access count
            count_key = f'count:{url}'
            count = redis_client.get(count_key) or 0
            count = int(count) + 1
            redis_client.set(count_key, count, ex=expiration)

            return result
        return wrapper
    return decorator


@cache_page(expiration=10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Example usage
    url = "http://slowwly.robertomurray.co.uk/"
    page_content = get_page(url)
    print(page_content)
