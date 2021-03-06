import click
from plex_trakt_sync.config import CONFIG
from plex_trakt_sync.logging import logging, measure_time
from plex_trakt_sync.main import process_movie_section, process_show_section
from plex_trakt_sync.plex_api import PlexApi
from plex_trakt_sync.trakt_api import TraktApi
from plex_trakt_sync.trakt_list_util import TraktListUtil


def sync():
    listutil = TraktListUtil()
    plex = PlexApi()
    trakt = TraktApi()

    with measure_time("Loaded Trakt lists"):
        trakt_watched_movies = trakt.watched_movies
        trakt_watched_shows = trakt.watched_shows
        trakt_movie_collection = trakt.movie_collection
        trakt_ratings = trakt.ratings
        trakt_watchlist_movies = trakt.watchlist_movies
        trakt_liked_lists = trakt.liked_lists

    if trakt_watchlist_movies:
        listutil.addList(None, "Trakt Watchlist", traktid_list=trakt_watchlist_movies)

    for lst in trakt_liked_lists:
        listutil.addList(lst['username'], lst['listname'])

    ps = plex.plex_server
    logging.info("Server version {} updated at: {}".format(ps.version, ps.updatedAt))
    logging.info("Recently added: {}".format(ps.library.recentlyAdded()[:5]))

    for section in plex.library_sections:
        if PlexApi.is_movie(section):
            with measure_time("Processing section %s" % section.title):
                process_movie_section(section, trakt_watched_movies, trakt_ratings, listutil, trakt_movie_collection)
        elif PlexApi.is_show(section):
            with measure_time("Processing section %s" % section.title):
                process_show_section(section, trakt_watched_shows, listutil)
        else:
            continue

    with measure_time("Updated plex watchlist"):
        listutil.updatePlexLists(ps)


@click.command()
def main():
    """
    Plex-Trakt-Sync is a two-way-sync between trakt.tv and Plex Media Server
    """

    logging.info("Starting sync Plex {} and Trakt {}".format(CONFIG['PLEX_USERNAME'], CONFIG['TRAKT_USERNAME']))

    with measure_time("Completed full sync"):
        sync()
