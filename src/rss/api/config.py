import os
from rss.utils.api_url import get_api_url
from rss.utils.env_variable import get_env_variable


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


class APIConfig:
    NAME = "dev"
    API_URL = get_api_url()
    # Flask and sql stuff
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_dev_postgres_uri(host=os.environ.get("DB_HOST", "localhost"))

    @staticmethod
    def init_app(app):
        pass


class DevAPIConfig(APIConfig):
    pass


class TestSQLiteConfig(APIConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProdAPIConfig(APIConfig):
    NAME = "prod"
    # Api config
    # Flask and sql stuff
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = get_postgres_uri()


api_configs = {
    "dev": DevAPIConfig(),
    "test-sqlite": TestSQLiteConfig(),
    "prod": ProdAPIConfig(),
}  # type: dict[str, Config]
