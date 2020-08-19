from hypothesis import given

from openapi_server.models import Status
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import sample_ids, statuses


@given(sample_id=sample_ids(), status=statuses())
def test_add_or_update_status_of_non_existent_sample(sample_id, status, add_or_replace_status):
    response = add_or_replace_status(sample_id, status)
    assert response.status_code == 404, response.data.decode()


@given(sample_id=sample_ids(), status=statuses())
def test_add_status(sample_id, status, create_sample_in_db, add_or_replace_status, get_status):
    with managed_db():
        create_sample_in_db(sample_id)

        response = add_or_replace_status(sample_id, status)
        added = Status.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert added == status

        response = get_status(sample_id)
        retrieved = Status.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert retrieved == added


@given(sample_id=sample_ids(), original=statuses(), new=statuses())
def test_replace_status(sample_id, original, new, create_sample_in_db, add_or_replace_status, get_status):
    with managed_db():
        create_sample_in_db(sample_id)
        add_or_replace_status(sample_id, original, ensure=True)

        response = add_or_replace_status(sample_id, new)
        updated = Status.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert updated == new

        response = get_status(sample_id)
        retrieved = Status.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert retrieved == updated


@given(sample_id=sample_ids())
def test_getting_statuses_of_non_existent_samples(sample_id, get_status):
    assert get_status(sample_id).status_code == 404


@given(sample_id=sample_ids())
def test_getting_non_existent_statuses(sample_id, create_sample_in_db, get_status):
    with managed_db():
        create_sample_in_db(sample_id)
        assert get_status(sample_id).status_code == 404


@given(sample_id=sample_ids(), status=statuses())
def test_getting_statuses(sample_id, status, create_sample_in_db, add_or_replace_status, get_status):
    with managed_db():
        create_sample_in_db(sample_id)
        add_or_replace_status(sample_id, status, ensure=True)

        response = get_status(sample_id)
        retrieved = Status.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert retrieved == status


@given(sample_id=sample_ids())
def test_deleting_status_of_non_existent_samples(sample_id, delete_status):
    response = delete_status(sample_id)
    assert response.status_code == 404


@given(sample_id=sample_ids())
def test_deleting_non_existent_statuses(sample_id, create_sample_in_db, delete_status):
    with managed_db():
        create_sample_in_db(sample_id)
        response = delete_status(sample_id)
        assert response.status_code == 404


@given(sample_id=sample_ids(), status=statuses())
def test_deleting_files(sample_id, status, create_sample_in_db, add_or_replace_status, delete_status, get_status):
    with managed_db():
        create_sample_in_db(sample_id)
        add_or_replace_status(sample_id, status, ensure=True)

        response = delete_status(sample_id)
        assert response.status_code == 204

        response = get_status(sample_id)
        assert response.status_code == 404


@given(sample_id=sample_ids(), status=statuses())
def test_update_status_of_non_existent_sample(sample_id, status, update_status):
    response = update_status(sample_id, status)
    assert response.status_code == 404, response.data.decode()


@given(sample_id=sample_ids(), original=statuses(), new=statuses())
def test_update_status(sample_id, original, new, create_sample_in_db, add_or_replace_status, update_status, get_status):
    new.stage = "deprecated"

    with managed_db():
        create_sample_in_db(sample_id)
        add_or_replace_status(sample_id, original, ensure=True)

        response = update_status(sample_id, new)
        updated = Status.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert updated == new

        response = get_status(sample_id)
        retrieved = Status.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert retrieved == updated