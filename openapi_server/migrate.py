from openapi_server.app import app
from openapi_server.db import db


def migrate(local_app):
    db.create_all(app=local_app.app)


if __name__ == '__main__':
    migrate(app)