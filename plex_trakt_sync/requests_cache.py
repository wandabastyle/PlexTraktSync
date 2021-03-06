import requests_cache
from .path import trakt_cache

requests_cache.install_cache(trakt_cache)


class CacheDisabledDecorator:
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args):
        with requests_cache.disabled():
            return self.fn(*args)
