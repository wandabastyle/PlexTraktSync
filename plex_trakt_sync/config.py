import json
from dotenv import load_dotenv
from os import getenv
from .path import config_file


class Config(dict):
    initialized = False

    def __getitem__(self, item):
        if not self.initialized:
            self.initialize()
        return dict.__getitem__(self, item)

    def initialize(self):
        with open(config_file, "r") as fp:
            config = json.load(fp)
            self.update(config)

        load_dotenv()
        if not getenv("PLEX_TOKEN") or not getenv("TRAKT_USERNAME"):
            print("First run, please follow those configuration instructions.")
            from get_env_data import get_env_data
            get_env_data()
            load_dotenv()

        self["PLEX_BASEURL"] = getenv("PLEX_BASEURL")
        self["PLEX_FALLBACKURL"] = getenv("PLEX_FALLBACKURL")
        self["PLEX_TOKEN"] = getenv("PLEX_TOKEN")
        self["PLEX_USERNAME"] = getenv("PLEX_USERNAME")
        self["TRAKT_USERNAME"] = getenv("TRAKT_USERNAME")

        self.initialized = True


CONFIG = Config()
