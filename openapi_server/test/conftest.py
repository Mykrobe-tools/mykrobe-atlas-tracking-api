import logging

import connexion
from pytest import fixture

from openapi_server.encoder import JSONEncoder


@fixture(scope='session')
def client():
    logging.getLogger('connexion.operation').setLevel('ERROR')
    app = connexion.App(__name__, specification_dir='../openapi/')
    app.app.json_encoder = JSONEncoder
    app.add_api('openapi.yaml')
    return app.app.test_client()
