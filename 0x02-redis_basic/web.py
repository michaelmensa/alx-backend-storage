#!/usr/bin/env python3
'''
Module web.py: Implementing an expiring web cache and tracker
'''
import requests
from functools import wraps
from typing import Callable
import redis


redis_client = redis.Redis()


def cache_page(func: Callable) -> Callable:
    ''' func the caches the output '''
    @wraps(func)
    def wrapper(url: str) -> str:
        ''' wrapper func for caching output '''
        redis_client.incr(f'count:{url}')
        cached_result = redis_client.get(f'page:{url}')
        if cached_result:
            return cached_result.decode('utf-8')
        cached_result = func(url)
        redis_client.set(f'count:{url}', 0)
        redis_client.setex(f'result:{url}', 10, cached_result)
        return cached_result
    return wrapper


@cache_page
def get_page(url: str) -> str:
    ''' returns the content of a URL after caching response '''
    response = requests.get(url)
    return response.text
