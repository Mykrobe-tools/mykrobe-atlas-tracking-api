from contextlib import contextmanager

from openapi_server.factories.db import db


@contextmanager
def managed_db():
    try:
        yield
    finally:
        db.drop_all()
        db.create_all()
