from hypothesis import given

from openapi_server.models import File
from openapi_server.test.assertions import assert_creating_secondary_resource_with_primary_resource
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import md5s, files, sample_ids


@given(md5sum=md5s())
def test_hash_does_not_exist(md5sum, get_file):
    assert get_file(md5sum).status_code == 404


@given(resource=files())
def test_hash_exists(resource, get_file, create_orphan_file):
    with managed_db():
        create_orphan_file(resource)

        response = get_file(resource.md5sum)
        assert response.status_code == 200

        created = File.from_dict(response.json)
        assert created == resource


@given(primary_pk_value=sample_ids(), secondary_resource=files())
def test_common_properties(primary_pk_value, secondary_resource, create_sample, create_file, get_file):
    assert_creating_secondary_resource_with_primary_resource(
        primary_pk_value, secondary_resource, create_primary=create_sample, create_secondary=create_file, get_secondary=get_file,
        strict_lookup=False, secondary_pk_name='md5sum')
