import logging

from hypothesis import settings
from pytest import fixture

from openapi_server.factories.app import create_app
from openapi_server.factories.db import db
from openapi_server.orm import Sample, File


@fixture
def app():
    logging.getLogger('connexion.operation').setLevel('ERROR')
    app = create_app()
    return app


@fixture
def client(app):
    return app.app.test_client()


@fixture
def make_request(client):
    def _(path, method, json=None, ensure=False, success_code=200):
        response = client.open(path=path, method=method, json=json)
        if ensure:
            assert response.status_code == success_code, response.data.decode()
        return response
    return _


@fixture
def list_events(make_request):
    def _(sample_id, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/events', 'GET', *args, **kwargs)
    return _


@fixture
def add_event(make_request):
    def _(sample_id, event, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/events', 'POST', json=event, success_code=201, *args, **kwargs)
    return _


@fixture
def get_event(make_request):
    def _(sample_id, event_id, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/events/{event_id}', 'GET', *args, **kwargs)
    return _


@fixture
def delete_event(make_request):
    def _(sample_id, event_id, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/events/{event_id}', 'DELETE', *args, **kwargs)
    return _


@fixture
def get_file(make_request):
    def _(md5sum, *args, **kwargs):
        return make_request(f'/api/v1/files/{md5sum}', 'GET', *args, **kwargs)
    return _


@fixture
def get_file_of_sample(make_request):
    def _(sample_id, md5sum, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/files/{md5sum}', 'GET', *args, **kwargs)
    return _


@fixture
def add_file(make_request):
    def _(sample_id, file, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/files', 'POST', json=file, success_code=201, *args, **kwargs)
    return _


@fixture
def list_files(make_request):
    def _(sample_id, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/files', 'GET', *args, **kwargs)
    return _


@fixture
def delete_file(make_request):
    def _(sample_id, md5sum, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/files/{md5sum}', 'DELETE', *args, **kwargs)
    return _


@fixture
def check_sample(make_request):
    def _(sample_id, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}', 'HEAD', *args, **kwargs)
    return _


@fixture
def add_or_replace_qc_result(make_request):
    def _(sample_id, qc_result, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/qc-result', 'PUT', json=qc_result, *args, **kwargs)
    return _


@fixture
def get_qc_result(make_request):
    def _(sample_id, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/qc-result', 'GET', *args, **kwargs)
    return _


@fixture
def delete_qc_result(make_request):
    def _(sample_id, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/qc-result', 'DELETE', *args, **kwargs)
    return _


@fixture
def add_or_replace_status(make_request):
    def _(sample_id, status, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/status', 'PUT', json=status, *args, **kwargs)
    return _


@fixture
def update_status(make_request):
    def _(sample_id, status, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/status', 'PATCH', json=status, *args, **kwargs)
    return _


@fixture
def get_status(make_request):
    def _(sample_id, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/status', 'GET', *args, **kwargs)
    return _


@fixture
def delete_status(make_request):
    def _(sample_id, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}/status', 'DELETE', *args, **kwargs)
    return _


@fixture
def create_sample(make_request):
    def _(sample, *args, **kwargs):
        return make_request(f'/api/v1/samples', 'POST', json=sample, *args, **kwargs)
    return _


@fixture
def get_sample(make_request):
    def _(sample_id, *args, **kwargs):
        return make_request(f'/api/v1/samples/{sample_id}', 'GET', *args, **kwargs)
    return _


@fixture
def get_resource(make_request):
    def _(uri, *args, **kwargs):
        return make_request(uri, 'GET', *args, **kwargs)
    return _


@fixture
def create_sample_in_db():
    def _(sample_id):
        inst = Sample(id=sample_id)
        db.session.add(inst)
        db.session.commit()
    return _


@fixture
def delete_sample():
    def _(sample_id):
        inst = Sample.query.get(sample_id)
        db.session.delete(inst)
        db.session.commit()
    return _


@fixture
def create_file():
    def _(model):
        inst = File.from_model(model)
        db.session.add(inst)
        db.session.commit()
    return _


settings.register_profile('e2e', deadline=None)
settings.load_profile('e2e')