from hypothesis import given

from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import sample_ids


@given(sample_id=sample_ids())
def test_sample_id_does_not_exist(sample_id, check_sample):
    response = check_sample(sample_id)
    assert response.status_code == 404


@given(sample_id=sample_ids())
def test_sample_exists(sample_id, create_sample, check_sample):
    with managed_db():
        create_sample(sample_id)

        response = check_sample(sample_id)
        assert response.status_code == 200