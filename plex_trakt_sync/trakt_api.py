import trakt
from plex_trakt_sync.path import pytrakt_file

trakt.core.CONFIG_PATH = pytrakt_file
import trakt.users
from trakt.errors import OAuthException, ForbiddenException

from plex_trakt_sync.requests_cache import requests_cache
from plex_trakt_sync.logging import logging
from plex_trakt_sync.memoize import Memoize as memoize


class TraktApi:
    """
    Trakt API class abstracting common data access and dealing with requests cache.
    """

    @property
    @memoize
    def me(self):
        with requests_cache.disabled():
            try:
                return trakt.users.User('me')
            except (OAuthException, ForbiddenException) as e:
                logging.fatal("Trakt authentication error: {}".format(str(e)))
                raise e
