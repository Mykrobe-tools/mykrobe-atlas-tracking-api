from openapi_server.app import app
from openapi_server.factories.db import db


def create_db(local_app):
    db.init_app(local_app.app)
    db.app = local_app.app
    db.create_all()


if __name__ == '__main__':
    create_db(app)