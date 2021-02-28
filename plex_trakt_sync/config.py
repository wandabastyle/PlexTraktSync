import json
from .path import config_file

with open(config_file, "r") as fp:
    CONFIG = json.load(fp)
