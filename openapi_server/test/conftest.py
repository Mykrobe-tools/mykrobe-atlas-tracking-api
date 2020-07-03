import logging

import connexion
from pytest import fixture

from openapi_server.db import init_db, migrate
from openapi_server.encoder import JSONEncoder


@fixture
def client():
    logging.getLogger('connexion.operation').setLevel('ERROR')

    app = connexion.App(__name__, specification_dir='../openapi/')
    app.app.json_encoder = JSONEncoder
    app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    with app.app.app_context():
        init_db(app.app)
        app.add_api('openapi.yaml')
        migrate()

    return app.app.test_client()
