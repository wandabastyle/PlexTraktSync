import click
from plex_trakt_sync.config import CONFIG
from plex_trakt_sync.logging import logging

@click.command()
def main():
    """
    Plex-Trakt-Sync is a two-way-sync between trakt.tv and Plex Media Server
    """

    logging.info("Starting sync Plex {} and Trakt {}".format(CONFIG['PLEX_USERNAME'], CONFIG['TRAKT_USERNAME']))
