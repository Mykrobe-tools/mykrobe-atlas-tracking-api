from hypothesis import given
from hypothesis.strategies import lists

from openapi_server.models import Sample
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import sample_ids, samples


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


@given(has_experiment_id_only=samples(has_isolate_id=False), has_isolate_id_only=samples(has_experiment_id=False),
       has_none=samples(has_experiment_id=False, has_isolate_id=False), has_both=samples(),
       unique_sample_ids=lists(sample_ids(), unique=True, min_size=4, max_size=4))
def test_listing_samples(has_experiment_id_only, has_isolate_id_only, has_none, has_both,
                         unique_sample_ids, create_sample, list_samples):
    has_experiment_id_only.id = unique_sample_ids[0]
    has_isolate_id_only.id = unique_sample_ids[1]
    has_none.id = unique_sample_ids[2]
    has_both.id = unique_sample_ids[3]

    assume(has_experiment_id_only.experiment_id != has_both.experiment_id)
    assume(has_isolate_id_only.isolate_id != has_both.isolate_id)

    with managed_db():
        create_sample(has_experiment_id_only, ensure=True, success_code=201)
        create_sample(has_isolate_id_only, ensure=True, success_code=201)
        create_sample(has_none, ensure=True, success_code=201)
        create_sample(has_both, ensure=True, success_code=201)

        has_experiment_ids = [Sample.from_dict(x) for x in list_samples(has_experiment_id=True, ensure=True).json]
        assert has_experiment_id_only in has_experiment_ids
        assert has_isolate_id_only not in has_experiment_ids
        assert has_none not in has_experiment_ids
        assert has_both in has_experiment_ids

        has_isolate_ids = [Sample.from_dict(x) for x in list_samples(has_isolate_id=True, ensure=True).json]
        assert has_experiment_id_only not in has_isolate_ids
        assert has_isolate_id_only in has_isolate_ids
        assert has_none not in has_isolate_ids
        assert has_both in has_isolate_ids

        has_nones = [Sample.from_dict(x) for x in list_samples(has_experiment_id=False, has_isolate_id=False, ensure=True).json]
        assert has_experiment_id_only not in has_nones
        assert has_isolate_id_only not in has_nones
        assert has_none in has_nones
        assert has_both not in has_nones

        has_boths = [Sample.from_dict(x) for x in
                     list_samples(has_experiment_id=True, has_isolate_id=True, ensure=True).json]
        assert has_experiment_id_only not in has_boths
        assert has_isolate_id_only not in has_boths
        assert has_none not in has_boths
        assert has_both in has_boths


@given(sample_id=sample_ids())
def test_getting_non_existent_samples(sample_id, get_sample):
    assert get_sample(sample_id).status_code == 404


@given(sample=samples())
def test_getting_samples(sample, create_sample, get_sample):
    with managed_db():
        response = create_sample(sample, ensure=True, success_code=201)

        response = get_sample(response.json['id'])
        retrieved = Sample.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert retrieved.experiment_id == sample.experiment_id
        assert retrieved.isolate_id == sample.isolate_id