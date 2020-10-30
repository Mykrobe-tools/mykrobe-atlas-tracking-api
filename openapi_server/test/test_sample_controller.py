import random

import pytest
from hypothesis import given, assume

from openapi_server.models import Sample
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import sample_ids, samples

SAMPLE_PROPS = ['experiment_id', 'isolate_id']
SAMPLE_UNIQUE_PROPS = ['experiment_id', 'isolate_id']


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


@given(sample_1=samples(), sample_2=samples())
def test_listing_samples_by_experiment_id(sample_1, sample_2, list_samples, create_sample):
    assume(sample_1.experiment_id != sample_2.experiment_id)

    # TODO: This can be deleted once the unique constraint for experiment/isolate IDs is removed
    assume(sample_1.isolate_id != sample_2.isolate_id)

    with managed_db():
        create_sample(sample_1, ensure=True, success_code=201)
        create_sample(sample_2, ensure=True, success_code=201)

        response = list_samples(experiment_id=sample_1.experiment_id)
        retrieved = [Sample.from_dict(x) for x in response.json]
        for x in retrieved:
            x.id = None

        assert response.status_code == 200
        assert sample_1 in retrieved
        assert sample_2 not in retrieved


@given(sample_1=samples(), sample_2=samples())
def test_listing_samples_by_isolate_id(sample_1, sample_2, list_samples, create_sample):
    assume(sample_1.isolate_id != sample_2.isolate_id)

    # TODO: This can be deleted once the unique constraint for experiment/isolate IDs is removed
    assume(sample_1.experiment_id != sample_2.experiment_id)

    with managed_db():
        create_sample(sample_1, ensure=True, success_code=201)
        create_sample(sample_2, ensure=True, success_code=201)

        response = list_samples(isolate_id=sample_1.isolate_id)
        retrieved = [Sample.from_dict(x) for x in response.json]
        for x in retrieved:
            x.id = None

        assert response.status_code == 200
        assert sample_1 in retrieved
        assert sample_2 not in retrieved


@pytest.mark.skip('current unique constraints make test construction impossible')
@given(with_experiment_id=samples(), with_isolate_id=samples(), with_both=samples())
def test_listing_samples_by_both_ids(with_experiment_id, with_isolate_id, with_both, list_samples, create_sample):
    assume(with_experiment_id.isolate_id != with_isolate_id.isolate_id and
           with_experiment_id.experiment_id != with_isolate_id.experiment_id)

    with_both.experiment_id = with_experiment_id.experiment_id
    with_both.isolate_id = with_isolate_id.isolate_id

    with managed_db():
        create_sample(with_experiment_id, ensure=True, success_code=201)
        create_sample(with_isolate_id, ensure=True, success_code=201)
        create_sample(with_both, ensure=True, success_code=201)

        response = list_samples(isolate_id=with_isolate_id.isolate_id, experiment_id=with_experiment_id.experiment_id)
        retrieved = [Sample.from_dict(x) for x in response.json]
        for x in retrieved:
            x.id = None

        assert response.status_code == 200
        assert with_experiment_id not in retrieved
        assert with_isolate_id not in retrieved
        assert with_both not in retrieved


@given(sample_1=samples(), sample_2=samples())
def test_listing_all_samples(sample_1, sample_2, list_samples, create_sample):
    # TODO: This can be deleted once the unique constraint for experiment/isolate IDs is removed
    assume(sample_1.isolate_id != sample_2.isolate_id)
    assume(sample_1.experiment_id != sample_2.experiment_id)

    with managed_db():
        create_sample(sample_1, ensure=True, success_code=201)
        create_sample(sample_2, ensure=True, success_code=201)

        response = list_samples()
        retrieved = [Sample.from_dict(x) for x in response.json]
        for x in retrieved:
            x.id = None

        assert response.status_code == 200
        assert sample_1 in retrieved
        assert sample_2 in retrieved


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


@given(sample_id=sample_ids(), sample=samples())
def test_patching_non_existent_samples(sample_id, sample, patch_sample):
    assert patch_sample(sample_id, sample).status_code == 404


@given(old_sample=samples(), another_sample=samples(), new_sample=samples())
def test_patching_samples_with_existing_unique_properties(old_sample, another_sample, new_sample, patch_sample, create_sample, get_sample):
    assume(old_sample.experiment_id != another_sample.experiment_id)
    assume(old_sample.isolate_id != another_sample.isolate_id)

    with managed_db():
        created = Sample.from_dict(create_sample(old_sample, ensure=True, success_code=201).json)
        create_sample(another_sample, ensure=True, success_code=201)

        prop = random.choice(SAMPLE_UNIQUE_PROPS)
        setattr(new_sample, prop, getattr(another_sample, prop))

        assert patch_sample(created.id, new_sample).status_code == 409

        retrieved = Sample.from_dict(get_sample(created.id, ensure=True).json)
        assert retrieved.experiment_id == old_sample.experiment_id
        assert retrieved.isolate_id == old_sample.isolate_id


@given(old_sample=samples(), new_sample=samples())
def test_patching_samples(old_sample, new_sample, patch_sample, create_sample, get_sample):
    to_keep = random.sample(SAMPLE_PROPS, random.randrange(0, len(SAMPLE_PROPS)))

    with managed_db():
        created = Sample.from_dict(create_sample(old_sample, ensure=True, success_code=201).json)

        for prop in to_keep:
            setattr(new_sample, prop, None)

        response = patch_sample(created.id, new_sample)
        patched = Sample.from_dict(response.json)

        assert response.status_code == 200
        for prop in SAMPLE_PROPS:
            if prop in to_keep:
                assert getattr(patched, prop) == getattr(old_sample, prop)
            else:
                assert getattr(patched, prop) == getattr(new_sample, prop)

        retrieved = Sample.from_dict(get_sample(created.id, ensure=True).json)
        assert retrieved == patched