#!/usr/bin/env python3

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class to interact with Redis for storing data with random keys.
    Automatically flushes the database on initialization.
    """

    def __init__(self):
        """
        Initializes the Redis client and flushes the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in Redis using a randomly generated UUID key.

        Args:
            data: The data to store (str, bytes, int, or float).

        Returns:
            The generated random key as a string.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key