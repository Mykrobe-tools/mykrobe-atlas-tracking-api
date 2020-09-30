from openapi_server.app import app
from openapi_server.db import db


def init_db(local_app):
    db.init_app(local_app.app)
    db.app = local_app.app
    db.create_all()


if __name__ == '__main__':
    init_db(app)