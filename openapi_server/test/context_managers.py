from contextlib import contextmanager

from openapi_server.db import db


@contextmanager
def managed_db():
    try:
        yield
    finally:
        db.drop_all()
        db.create_all()
