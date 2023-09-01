from typing import Type
import os

base_path = os.path.dirname(__file__)


class MissingEnvVariableError(ValueError):
    pass


def get_env_variable(name: str, var_type: Type[str] | Type[int] = str) -> str | int:
    """ Check that an environment variable is set in production mode.
    """
    config = os.environ.get("CONFIG", "dev")
    if "prod" in config:
        value = os.environ.get(name, None)
        if value is None:
            raise MissingEnvVariableError(
                f"The env variable {name} is necessary to run the app"
            )
        if var_type is str:
            return value
        elif var_type is int:
            return int(var_type)
        raise ValueError(f"Invalid var type {var_type}")

    if var_type is str:
        return ""
    elif var_type is int:
        return 0
    raise ValueError(f"Invalid var type {var_type}")


def get_api_url() -> str:
    host = os.environ.get("API_HOST", "localhost")
    port = 5000 if host == "localhost" else 80
    return f"http://{host}:{port}"


def get_dev_postgres_uri(host: str = "localhost") -> str:
    password = os.environ.get("DB_PASSWORD", "abc123")
    if host == "localhost":
        port = 54321
    else:
        # Port of the database in the docker container
        port = 5432
    user, db_name = "rss", "rss"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_postgres_uri() -> str:
    """ Get the postgres uri for the production database. """
    host = get_env_variable("DB_HOST")
    user = get_env_variable("DB_USER")
    password = get_env_variable("DB_PASSWORD")
    port = get_env_variable("DB_PORT")
    db_name = get_env_variable("DB_NAME")
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

    IP = get_env_variable("CLIENT_IP")
    PORT = get_env_variable("CLIENT_PORT", int)

    API_URL = get_env_variable("API_HOST")
    API_USER = get_env_variable("API_USER")
    API_PASSWORD = get_env_variable("API_PASSWORD")

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
