import redis
from os import getenv
import config

pool = None

def init():
    global pool
    pool = redis.ConnectionPool(host=config.redis_host, port=config.redis_port)
    return pool

def get_redis():
    return redis.Redis(connection_pool=pool)

def delete_keys(keys):
    conn = get_redis()
    for key in keys:
        conn.delete(key)

def delete_keys_pattern(patterns):
    redis = get_redis()
    for pattern in patterns:
        keys = redis.keys(pattern)
        if (len(keys)):
            redis.delete(*keys)
