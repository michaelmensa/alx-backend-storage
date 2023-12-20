#!/usr/bin/env python3
'''
Module  Cache: Building a cache system in steps
'''
import redis
import uuid
from typing import Union, Callable, Optional


class Cache():
    '''
    The cache class: for caching
    '''
    def __init__(self):
        '''
        constructor method
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        function that stores and returns string
        '''
        r_key = str(uuid.uuid4())
        self._redis.set(r_key, data)
        return r_key

    def get(self, key: str, fn: Optional[Callable] = None):
        '''
        writing our own get function, different from the one from redis
        we need get_str and get_int to automatically parametrize Cache.get
        with the correct conversion
        '''
        result = self._redis.get(key)
        if result is not None and fn is not None:
            return fn(result)
        return result

    def get_str(self, key: str) -> Union[str, None]:
        ''' get_str function automatically parametrize Cache.get with the
        correct conversion function
        '''
        x = self.get(key,
                     fn=lambda d: d.decode('utf-8') if d is not None else None)
        return x

    def get_int(self, key: str) -> Union[int, None]:
        ''' get_int func automatically parametrize Cache.get with the
        correct conversion function
        '''
        return self.get(key,
                        fn=lambda d: int(d) if d is not None else None)
