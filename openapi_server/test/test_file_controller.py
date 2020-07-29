from hypothesis import given
from hypothesis.strategies import lists, sets

from openapi_server.models import File
from openapi_server.test.scenarios import check_creating_secondary_resource_scenarios, \
    check_listing_secondary_resources_scenarios, check_getting_secondary_resource_of_non_existent_primary_resource, \
    check_getting_non_existent_secondary_resource, check_getting_secondary_resource
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
    check_creating_secondary_resource_scenarios(
        primary_pk_value, secondary_resource, create_primary=create_sample, create_secondary=create_file, get_secondary=get_file,
        strict_lookup=False, secondary_pk_name='md5sum')


@given(primary_pk_values=sets(sample_ids(), min_size=2, max_size=2), secondary_resources=lists(files(), min_size=1, unique_by=lambda x: x.md5sum))
def test_listing_behaviours(primary_pk_values, secondary_resources, create_sample, create_file, list_files):
    check_listing_secondary_resources_scenarios(primary_pk_values, secondary_resources, create_sample, create_file, list_files)


@given(sample_id=sample_ids(), file=files())
def test_getting_files_of_non_existent_samples(sample_id, file, get_file_of_sample, create_file, create_sample, delete_sample):
    check_getting_secondary_resource_of_non_existent_primary_resource(sample_id, file, get_file_of_sample, create_file, create_sample, delete_sample, secondary_pk_name='md5sum')


@given(sample_id=sample_ids(), file=files())
def test_getting_non_existent_files(sample_id, file, get_file_of_sample, create_sample):
    check_getting_non_existent_secondary_resource(sample_id, file, get_file_of_sample, create_sample, secondary_pk_name='md5sum')


@given(sample_id=sample_ids(), file=files())
def test_getting_files(sample_id, file, get_file_of_sample, create_file, create_sample):
    check_getting_secondary_resource(sample_id, file, get_file_of_sample, create_file, create_sample, secondary_pk_name='md5sum')


@given(sample_id=sample_ids(), file=files())
def test_deleting_files_of_non_existent_samples(sample_id, file, delete_file, create_file, create_sample, delete_sample):
    with managed_db():
        create_sample(sample_id)
        create_file(sample_id, file, ensure=True)
        delete_sample(sample_id)

        response = delete_file(sample_id, file.md5sum)
        assert response.status_code == 404


@given(sample_id=sample_ids(), file=files())
def test_deleting_non_existent_events(sample_id, file, delete_file, create_sample):
    with managed_db():
        create_sample(sample_id)
        response = delete_file(sample_id, file.md5sum)
        assert response.status_code == 404


@given(sample_id=sample_ids(), file=files())
def test_deleting_events(sample_id, file, delete_file, create_file, create_sample, get_file):
    with managed_db():
        create_sample(sample_id)
        create_file(sample_id, file, ensure=True)

        response = delete_file(sample_id, file.md5sum)
        assert response.status_code == 204

        response = get_file(sample_id, file.md5sum)
        assert response.status_code == 404