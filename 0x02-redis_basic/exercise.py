#!/usr/bin/env python3

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        return output
    return wrapper

def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function."""
    r = redis.Redis()
    method_name = method.__qualname__
    calls = r.get(method_name)
    try:
        calls = int(calls.decode('utf-8'))
    except Exception:
        calls = 0
    print(f"{method_name} was called {calls} times:")
    inputs = r.lrange(f"{method_name}:inputs", 0, -1)
    outputs = r.lrange(f"{method_name}:outputs", 0, -1)
    for inp, out in zip(inputs, outputs):
        print(f"{method_name}(*{inp.decode('utf-8')}) -> {out.decode('utf-8')}")




class Cache:

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()


    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
       
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    
    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data
    
    def get_str(self, key: str) -> Optional[str]:
        return self.get(key, fn=lambda d: d.decode('utf-8'))
    
    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=int)
    
