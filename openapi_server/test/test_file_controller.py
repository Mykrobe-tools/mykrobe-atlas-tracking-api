from hypothesis import given

from openapi_server.models import File
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import md5s, files


@given(md5sum=md5s())
def test_hash_does_not_exist(md5sum, get_file):
    assert get_file(md5sum).status_code == 404


@given(resource=files())
def test_hash_exists(resource, get_file, create_file):
    with managed_db():
        create_file(resource)

        response = get_file(resource.md5sum)
        assert response.status_code == 200

        created = File.from_dict(response.json)
        assert created == resource