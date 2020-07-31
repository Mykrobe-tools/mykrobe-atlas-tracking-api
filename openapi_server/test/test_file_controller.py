import random

from hypothesis import given
from hypothesis.strategies import lists, sets

from openapi_server.models import File
from openapi_server.test.assertions import assert_equal_lists
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import md5s, files, sample_ids


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


@given(sample_id=sample_ids(), file=files())
def test_adding_files_to_non_existent_sample(sample_id, file, add_file):
    response = add_file(sample_id, file)
    assert response.status_code == 404


@given(sample_id=sample_ids(), file=files())
def test_adding_files(sample_id, file, create_sample, add_file, get_file_of_sample):
    with managed_db():
        create_sample(sample_id)

        response = add_file(sample_id, file)
        assert response.status_code == 201

        created = File.from_dict(response.json)
        assert created == file

        response = get_file_of_sample(sample_id, created.md5sum)
        assert response.status_code == 200

        retrieved = File.from_dict(response.json)
        assert retrieved == created


@given(sample_id=sample_ids(), file=files())
def test_adding_duplicated_files(sample_id, file, create_sample, add_file):
    with managed_db():
        create_sample(sample_id)
        add_file(sample_id, file, ensure=True)

        response = add_file(sample_id, file)
        assert response.status_code == 409


@given(sample_id=sample_ids())
def test_listing_files_of_non_existent_sample(sample_id, list_files):
    response = list_files(sample_id)
    assert response.status_code == 404


@given(sample_id_pair=sets(sample_ids(), min_size=2, max_size=2),
       file_list=lists(files(), min_size=1, unique_by=lambda x: x.md5sum))
def test_listing_files(sample_id_pair, file_list, create_sample, add_file,
                        list_files):
    sample_id, other_sample_id = sample_id_pair
    associated_files = random.sample(file_list, random.randrange(0, len(file_list)))

    with managed_db():
        create_sample(sample_id)
        create_sample(other_sample_id)

        for file in file_list:
            if file in associated_files:
                add_file(sample_id, file, ensure=True)
            else:
                add_file(other_sample_id, file, ensure=True)

        response = list_files(sample_id)
        assert response.status_code == 200

        listed = [file.from_dict(x) for x in response.json]
        assert_equal_lists(listed, associated_files)


@given(sample_id=sample_ids(), file=files())
def test_getting_files_of_non_existent_samples(sample_id, file, get_file_of_sample, add_file, create_sample, delete_sample):
    with managed_db():
        create_sample(sample_id)
        add_file(sample_id, file, ensure=True)
        delete_sample(sample_id)

        response = get_file_of_sample(sample_id, file.md5sum)
        assert response.status_code == 404


@given(sample_id=sample_ids(), file=files())
def test_getting_non_existent_files(sample_id, file, get_file_of_sample, create_sample):
    with managed_db():
        create_sample(sample_id)
        response = get_file_of_sample(sample_id, file.md5sum)
        assert response.status_code == 404


@given(sample_id=sample_ids(), file=files())
def test_getting_files(sample_id, file, get_file_of_sample, add_file, create_sample):
    with managed_db():
        create_sample(sample_id)
        add_file(sample_id, file, ensure=True)

        response = get_file_of_sample(sample_id, file.md5sum)
        assert response.status_code == 200

        created = File.from_dict(response.json)
        assert created == file


@given(sample_id=sample_ids(), file=files())
def test_deleting_files_of_non_existent_samples(sample_id, file, delete_file, create_file):
    with managed_db():
        create_file(file)

        response = delete_file(sample_id, file.md5sum)
        assert response.status_code == 404


@given(sample_id=sample_ids(), file=files())
def test_deleting_non_existent_files(sample_id, file, delete_file, create_sample):
    with managed_db():
        create_sample(sample_id)
        response = delete_file(sample_id, file.md5sum)
        assert response.status_code == 404


@given(sample_id=sample_ids(), file=files())
def test_deleting_files(sample_id, file, delete_file, add_file, create_sample, get_file):
    with managed_db():
        create_sample(sample_id)
        add_file(sample_id, file, ensure=True)

        response = delete_file(sample_id, file.md5sum)
        assert response.status_code == 204

        response = get_file(sample_id, file.md5sum)
        assert response.status_code == 404