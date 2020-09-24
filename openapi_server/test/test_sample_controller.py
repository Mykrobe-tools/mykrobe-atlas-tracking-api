from uuid import UUID

from hypothesis import given, assume, settings, HealthCheck

from openapi_server.models import Sample
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import sample_ids, samples, safe_strings


@given(sample_id=sample_ids())
def test_sample_id_does_not_exist(sample_id, check_sample):
    response = check_sample(sample_id)
    assert response.status_code == 404


@given(sample_id=sample_ids())
def test_sample_exists(sample_id, create_sample_in_db, check_sample):
    with managed_db():
        create_sample_in_db(sample_id)

        response = check_sample(sample_id)
        assert response.status_code == 200


@given(sample=samples())
def test_creating_samples(sample, create_sample, check_sample, get_resource):
    with managed_db():
        response = create_sample(sample)
        created = Sample.from_dict(response.json)

        assert response.status_code == 201
        assert created.experiment_id == sample.experiment_id
        assert created.isolate_id == sample.isolate_id

        from_location_header = Sample.from_dict(get_resource(response.location, ensure=True).json)
        assert created == from_location_header

        response = check_sample(created.id)
        assert response.status_code == 200


@given(existed=samples(), duplicated_exp_id=samples(), duplicated_isolate_id=samples())
def test_creating_duplicated_samples(existed, duplicated_exp_id, duplicated_isolate_id, create_sample):
    duplicated_exp_id.experiment_id = existed.experiment_id
    duplicated_isolate_id.isolate_id = existed.isolate_id

    with managed_db():
        create_sample(existed, ensure=True, success_code=201)

        response = create_sample(duplicated_exp_id)
        assert response.status_code == 409

        response = create_sample(duplicated_isolate_id)
        assert response.status_code == 409


@given(sample_id=sample_ids())
def test_getting_non_existent_samples(sample_id, get_sample):
    assert get_sample(sample_id).status_code == 404


@settings(suppress_health_check=(HealthCheck.filter_too_much,))
@given(sample_id=safe_strings(min_size=1))
def test_invalid_sample_id(sample_id, get_sample):
    def is_uuid(s):
        try:
            UUID(s, version=4)
        except ValueError:
            return False
        else:
            return True
    assume(not is_uuid(sample_id))

    assert get_sample(sample_id).status_code == 400


@given(sample=samples())
def test_getting_samples(sample, create_sample, get_sample):
    with managed_db():
        response = create_sample(sample, ensure=True, success_code=201)

        response = get_sample(response.json['id'])
        retrieved = Sample.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert retrieved.experiment_id == sample.experiment_id
        assert retrieved.isolate_id == sample.isolate_id