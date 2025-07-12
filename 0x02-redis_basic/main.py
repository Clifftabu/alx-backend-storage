#!/usr/bin/env python3
"""
Main file for testing Cache class storage in Redis
"""

import redis

Cache = __import__('exercise').Cache
replay = __import__('exercise').replay

# Use one Cache instance throughout to avoid flushdb wiping prior data
cache = Cache()

"""
1st test for task 0
"""
data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))

"""
2nd test for task 1
"""
TEST_CASES = {
    b"foo": None,
    123: lambda d: int(d.decode("utf-8")),
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value

print("All test cases for Task 1 passed successfully.")

"""
Main file for Task 2
"""
cache.store(b"first")
print(cache.get(cache.store.__qualname__))

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))

"""
Main file for Task 3
"""
s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store("third")
print(s3)

inputs = cache._redis.lrange(f"{cache.store.__qualname__}:inputs", 0, -1)
outputs = cache._redis.lrange(f"{cache.store.__qualname__}:outputs", 0, -1)

print("inputs:", inputs)
print("outputs:", outputs)

"""
Main file for Task 4: Replay
"""
cache.store("foo")
cache.store("bar")
cache.store(42)

replay(cache.store)
