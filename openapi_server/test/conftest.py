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
def make_request(client):
    def _(path, method, json=None, ensure=False, success_code=200):
        response = client.open(path=path, method=method, json=json)
        if ensure:
            assert response.status_code == success_code
        return response
    return _


@fixture
def list_event(make_request):
    def _(sample_id, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/events', 'GET', *args, **kwargs)
    return _


@fixture
def create_event(make_request):
    def _(sample_id, event, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/events', 'POST', json=event, success_code=201, *args, **kwargs)
    return _


@fixture
def get_event(make_request):
    def _(sample_id, event_id, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/events/{event_id}', 'GET', *args, **kwargs)
    return _


@fixture
def create_sample():
    def _(sample_id):
        sample = Sample(id=sample_id)
        db.session.add(sample)
        db.session.commit()
    return _


@fixture
def delete_sample():
    def _(sample_id):
        sample = Sample.query.get(sample_id)
        db.session.delete(sample)
        db.session.commit()
    return _
