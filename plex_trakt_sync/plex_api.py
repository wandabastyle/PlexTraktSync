from plexapi.library import MovieSection, ShowSection
from plex_trakt_sync.memoize import Memoize as memoize
from plex_trakt_sync.requests_cache import CacheDisabledDecorator as nocache
from plex_trakt_sync.main import get_plex_server
from plex_trakt_sync.config import CONFIG


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
        result = []
        for section in self.plex_server.library.sections():
            if section.title in CONFIG["excluded-libraries"]:
                continue
            result.append(section)

        return result

    @staticmethod
    def is_movie(section):
        return type(section) is MovieSection

    @staticmethod
    def is_show(section):
        return type(section) is ShowSection
