import os
from rss.config import DevConfig, ProdConfig

config_type = os.environ.get("CONFIG", "dev")

if config_type == "dev":
    CONFIG = DevConfig()
elif config_type == "prod":
    CONFIG = ProdConfig()
else:
    raise ValueError(f"Incorrect config type {config}")
