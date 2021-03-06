from contextlib import contextmanager
import logging
import sys
from .config import CONFIG
from .path import log_file
from time import time


@contextmanager
def measure_time(message, level=logging.INFO):
    start = time()
    yield
    timedelta = time() - start

    m, s = divmod(timedelta, 60)
    logging.log(level, message + " in " + (m > 0) * "{:.0f} min ".format(m) + (s > 0) * "{:.1f} seconds".format(s))


def initialize():
    # global log level for all messages
    log_level = logging.DEBUG if CONFIG['log_debug_messages'] else logging.INFO
    log_format = '%(asctime)s %(levelname)s:%(message)s'

    # messages with info and above are printed to stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    console_handler.setLevel(logging.INFO)

    # file handler can log down to debug messages
    file_handler = logging.FileHandler(log_file, 'w', 'utf-8')
    file_handler.setLevel(logging.DEBUG)

    handlers = [
        file_handler,
        console_handler,
    ]
    logging.basicConfig(format=log_format, handlers=handlers, level=log_level)


initialize()
