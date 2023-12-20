#!/usr/bin/env python3
'''
Module  Cache: Building a cache system in steps
'''
import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def replay(func: Callable) -> None:
    '''
    function to display the history of calls of a particular function
    '''
    # check if func is of __self__
    if func is None or not hasattr(func, '__self__'):
        return

    # check if func is of Redis
    history = getattr(func.__self__, 'redis', None)
    if not isinstance(history, redis.Redis):
        return

    i_key = f'{func.__qualname__}:inputs'
    o_key = f'{func.__qualname__}:outputs'
    count = 0

    if history.exists(func.__qualname__) != 0:
        count = int(history.get(func.__qualname__))
    print(f'{func.__qualname__} was called {count} times:')

    inputs = history.lrange(i_key, 0, -1)
    outputs = history.lrange(o_key, 0, -1)

    for i, o in zip(inputs, outputs):
        print(f'{func.__qualname__}(*{i.decode("utf-8")})
              -> {o.decode('utf-8')}')


def count_calls(method: Callable) -> Callable:
    '''
    decorator function that takes method arg and returns callable
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''
        wrapper func, invokes name of method using __qualname__
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''
    decorator function to store history of inputs and outputs for a
    particular function
    '''
    @wraps(method)
    def wrapper(self, *args) -> Any:
        '''
        wrapper func, invokes method name using qualified name.
        use lpush for inputs and rpush for outputs
        '''
        i_key = f'{method.__qualname__}:inputs'
        o_key = f'{method.__qualname__}:outputs'
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(i_key, str(args))
        result = method(self, *args)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(o_key, result)
        return result
    return wrapper


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

    @count_calls
    @call_history
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
