from plex_trakt_sync.memoize import Memoize as memoize
from plex_trakt_sync.requests_cache import CacheDisabledDecorator as nocache
from plex_trakt_sync.main import get_plex_server


class PlexApi:
    """
    Plex API class abstracting common data access and dealing with requests cache.
    """

    @property
    @memoize
    @nocache
    def plex_server(self):
        return get_plex_server()

    @property
    @memoize
    @nocache
    def library_sections(self):
        return self.plex_server.library.sections()
