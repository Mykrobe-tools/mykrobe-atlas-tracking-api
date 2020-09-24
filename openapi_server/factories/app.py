import os

import connexion
from werkzeug.exceptions import InternalServerError

from openapi_server import encoder
from openapi_server.factories.db import db
from openapi_server.error_handlers import internal_server_error_handler


def create_app():
    app = connexion.App(__name__, specification_dir='../openapi/')
    app.app.json_encoder = encoder.JSONEncoder

    app.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://postgres@localhost:5432')
    db.init_app(app.app)
    db.app = app.app

    app.add_api('openapi.yaml', arguments={'title': 'Tracking API'})
    db.create_all()

    app.add_error_handler(InternalServerError, internal_server_error_handler)

    return app