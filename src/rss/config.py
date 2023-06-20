import os


base_path = os.path.dirname(__file__)


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5000 if host == "localhost" else 80
    return f"http://{host}:{port}"


def get_dev_postgres_uri(host: str = "localhost") -> str:
    password = os.environ.get("DB_PASSWORD", "abc123")
    if host == "localhost":
        port = 54321
    else:
        port = 5432
    user, db_name = "rss", "rss"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_postgres_uri() -> str:
    host = os.environ.get("DB_HOST", "localhost")
    user = os.environ.get("DB_USER", "rss")
    password = os.environ.get("DB_PASSWORD", "abc123")
    port = os.environ.get("DB_PORT", 5432)
    db_name = os.environ.get("DB_NAME", "rss")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


class Config:
    # rss.main.py config
    ALERT_TIME = int(os.environ.get("ALERT_TIME", 5))
    MSG_TIME = int(os.environ.get("MSG_TIME", 5))
    ALERT_FILE_NAME = "test_alert"
    UPDATE_FILE_NAME = "test_update"
    EVENT_FILE_NAME = "test_event"
    EVENT_UPDATE_FILE_NAME = "test_event_update"

    IP = os.environ.get("IP", "localhost")
    PORT = int(os.environ.get("PORT", 12345))

    API_URL = get_api_url()
    API_USER = "triton"
    API_PASSWORD = "abc123"

    SAVE_PATH = os.path.abspath(os.path.join(base_path, "..", "..", "feeds/"))
    POST_API_PATH = os.environ.get("POST_API_PATH", "")

    # API config
    # Flask and sql stuff
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_dev_postgres_uri(host=os.environ.get("DB_HOST", "localhost"))

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    pass


class TestSQLiteConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProdConfig(Config):
    # rss.main.py config
    ALERT_TIME = 60
    MSG_TIME = 60
    ALERT_FILE_NAME = "sasmex"
    UPDATE_FILE_NAME = "sasmex"
    EVENT_FILE_NAME = "sasmex_evento"
    EVENT_UPDATE_FILE_NAME = "sasmex_evento"

    IP = "172.30.17.182"
    PORT = 13084

    API_URL = get_api_url()
    API_USER = os.environ.get("API_USER")
    API_PASSWORD = os.environ.get("API_PASSWORD")

    SAVE_PATH = os.environ.get("SAVE_PATH", Config.SAVE_PATH)
    POST_API_PATH = os.environ.get("POST_API_PATH", "")

    # Api config
    # Flask and sql stuff
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = get_postgres_uri()


configurations = {
    "dev": DevConfig(),
    "test-sqlite": TestSQLiteConfig(),
    "prod": ProdConfig(),
}  # type: dict[str, Config]
