import os
from rss.config import configurations

config_type = os.environ.get("CONFIG", "dev")

try:
    CONFIG = configurations[config_type]
except KeyError:
    raise ValueError(f"Incorrect config type {config}")
