import redis
from django.conf import settings
from django.core.cache import cache


def cache_set(key, value):
    try:
        cache.set(key, value, settings.USER_CACHE_TIMEOUT)
    except (redis.exceptions.TimeoutError, redis.exceptions.ConnectionError):
        pass


def cache_get_or_set(key, func, **kwargs):
    try:
        value = cache.get(key)
        if value is None:
            value = func(**kwargs)
            cache_set(key, value)
        return value
    except (redis.exceptions.TimeoutError, redis.exceptions.ConnectionError):
        return func(**kwargs)
