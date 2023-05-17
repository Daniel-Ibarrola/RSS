import time
import pytest
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

from rss import CONFIG
from rss.api import create_app, db


@pytest.fixture
def wait_for_api():
    start = time.time()
    url = CONFIG.API_URL
    while time.time() - start < 10:
        try:
            requests.get(url)
            return
        except requests.ConnectionError:
            continue

    pytest.fail("Could not connect to API")


def wait_for_postgres():
    engine = create_engine(CONFIG.POSTGRES_URI)
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            engine.connect()
            return engine
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Postgres never came up")


def create_app_and_db():
    app = create_app(CONFIG)
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    return app_context


def tear_down(app_context):
    db.session.remove()
    db.drop_all()
    app_context.pop()


@pytest.fixture
def sqlite_session():
    app_context = create_app_and_db()
    yield
    tear_down(app_context)


@pytest.fixture(scope="session")
def postgres_db():
    engine = wait_for_postgres()
    return engine


@pytest.fixture
def postgres_session(postgres_db):
    session = sessionmaker(bind=postgres_db)()
    yield session

    # Clear database after running tests
    session.execute(text("DELETE FROM events"))
    session.commit()
    session.close()
