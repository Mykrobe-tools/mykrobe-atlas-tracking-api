import logging

import connexion
from pytest import fixture

from openapi_server.db import db
from openapi_server.encoder import JSONEncoder
from openapi_server.orm import Sample


@fixture
def client():
    logging.getLogger('connexion.operation').setLevel('ERROR')
    app = connexion.App(__name__, specification_dir='../openapi/')
    app.app.json_encoder = JSONEncoder

    app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    db.init_app(app.app)
    db.app = app.app

    app.add_api('openapi.yaml')
    db.create_all()

    return app.app.test_client()


@fixture
def create_event(client):
    def _(sample_id, event):
        return client.post(f'/api/v1/samples/{sample_id}/events', json=event)
    return _


@fixture
def get_event(client):
    def _(sample_id, event_id):
        return client.get(f'/api/v1/samples/{sample_id}/events/{event_id}')
    return _


@fixture
def create_sample():
    def _(sample_id):
        sample = Sample(id=sample_id)
        db.session.add(sample)
        db.session.commit()
    return _
