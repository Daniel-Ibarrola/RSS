from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import OperationalError
import time


def wait_for_postgres(postgres_uri: str) -> Engine:
    engine = create_engine(postgres_uri)
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            engine.connect()
            return engine
        except OperationalError:
            time.sleep(0.5)

    raise ValueError(
        f"Failed to connect to database in {postgres_uri}"
    )
