import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


base_path = os.path.dirname(__file__)


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5000 if host == "localhost" else 80
    return f"http://{host}:{port}"


def get_postgres_uri(host: str = "localhost"):
    password = os.environ.get("DB_PASSWORD", "abc123")
    if host == "localhost":
        port = 54321
    else:
        port = 5432
    user, db_name = "rss", "rss"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


class DevConfig(Config):
    ALERT_TIME = int(os.environ.get("ALERT_TIME", 5))
    MSG_TIME = int(os.environ.get("MSG_TIME", 5))
    ALERT_FILE_NAME = "test_alert"
    UPDATE_FILE_NAME = "test_update"
    EVENT_FILE_NAME = "test_event"
    EVENT_UPDATE_FILE_NAME = "test_event_update"
    IP = os.environ.get("IP", "localhost")
    PORT = int(os.environ.get("PORT", 12345))
    SAVE_PATH = os.path.abspath(os.path.join(base_path, "..", "..", "feeds/"))
    CHECK_LAST_ALERT = False
    # Flask and sql stuff
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_postgres_uri(host=os.environ.get("DB_HOST", "localhost"))
    API_URL = get_api_url()


class ProdConfig(Config):
    ALERT_TIME = 60
    MSG_TIME = 60
    ALERT_FILE_NAME = "sasmex"
    UPDATE_FILE_NAME = "sasmex"
    EVENT_FILE_NAME = "sasmex_evento"
    EVENT_UPDATE_FILE_NAME = "sasmex_evento"
    IP = "172.30.17.182"
    PORT = 13084
    SAVE_PATH = "/var/www/rss/"
    CHECK_LAST_ALERT = False
    # Flask and sql stuff
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = get_postgres_uri(host=os.environ.get("DB_HOST", "localhost"))
    API_URL = get_api_url()


configurations = {
    "dev": DevConfig(),
    "prod": ProdConfig(),
}
