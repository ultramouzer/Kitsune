import redis
from os import getenv

from configs.env_vars import redis_host, redis_port

pool = None

def init():
    global pool
    pool = redis.ConnectionPool(host=redis_host, port=redis_port)
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
