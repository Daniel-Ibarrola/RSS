import os
from rss.utils.api_url import get_api_url
from rss.utils.env_variable import get_env_variable


base_path = os.path.dirname(__file__)


class Config:
    # rss.main.py config
    ALERT_TIME = int(os.environ.get("ALERT_TIME", 5))
    MSG_TIME = int(os.environ.get("MSG_TIME", 5))
    ALERT_FILE_NAME = "test_alert"
    UPDATE_FILE_NAME = "test_update"
    EVENT_FILE_NAME = "test_event"
    EVENT_UPDATE_FILE_NAME = "test_event_update"

    IP = os.environ.get("CLIENT_IP", "localhost")
    PORT = int(os.environ.get("CLIENT_PORT", 12345))

    API_URL = get_api_url()
    API_USER = "triton"
    API_PASSWORD = "abc123"

    SAVE_PATH = os.path.abspath(os.path.join(base_path, "..", "..", "feeds/"))
    POST_API_PATH = os.environ.get("POST_API_PATH", "")

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    pass


class ProdConfig(Config):
    # rss.main.py config
    ALERT_TIME = 60
    MSG_TIME = 60
    ALERT_FILE_NAME = "sasmex"
    UPDATE_FILE_NAME = "sasmex"
    EVENT_FILE_NAME = "sasmex_evento"
    EVENT_UPDATE_FILE_NAME = "sasmex_evento"

    IP = get_env_variable("CLIENT_IP")
    PORT = get_env_variable("CLIENT_PORT", int)

    API_URL = get_env_variable("API_HOST")
    API_USER = get_env_variable("API_USER")
    API_PASSWORD = get_env_variable("API_PASSWORD")

    SAVE_PATH = os.environ.get("SAVE_PATH", Config.SAVE_PATH)
    POST_API_PATH = os.environ.get("POST_API_PATH", "")


configurations = {
    "dev": DevConfig(),
    "prod": ProdConfig(),
}  # type: dict[str, Config]
