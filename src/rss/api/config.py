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
    """ Configuration for the API.

        It declares postgres URI and the API server URl. It also declares other
        configuration parameters needed for flask and sql-alchemy.
    """
    NAME = "dev"
    API_URL = get_api_url()
    API_USER = "triton"
    API_PASSWORD = "dog"
    # Flask and sql stuff
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_dev_postgres_uri(
        host=os.environ.get("DB_HOST", "localhost")
    )

    @staticmethod
    def init_app(app):
        pass


class DevAPIConfig(APIConfig):
    pass


class TestSQLiteConfig(APIConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProdAPIConfig(APIConfig):
    """ Configuration for the API in production.

        It declares postgres URI and the API server URl. It also declares other
        configuration parameters needed for flask and sql-alchemy.

        The following environmental variables need to be defined:

        - DB_HOST
        - DB_USER
        - DB_PASSWORD
        - DB_PORT
        - DB_NAME
        - API_USER
        - API_PASSWORD

        Optionally, API_HOST may need to be defined. Defaults to localhost.
    """
    NAME = "prod"

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = get_postgres_uri()
    API_USER = get_env_variable("API_USER")
    API_PASSWORD = get_env_variable("API_PASSWORD")


api_configs = {
    "dev": DevAPIConfig(),
    "test-sqlite": TestSQLiteConfig(),
    "prod": ProdAPIConfig(),
}  # type: dict[str, APIConfig]
