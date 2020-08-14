from hypothesis import given

from openapi_server.models import Sample
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import sample_ids, samples


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


@given(sample=samples())
def test_creating_samples(sample, create_sample_, check_sample):
    with managed_db():
        response = create_sample_(sample)
        created = Sample.from_dict(response.json)

        assert response.status_code == 201
        assert created.experiment_id == sample.experiment_id
        assert created.isolate_id == sample.isolate_id

        # response = check_sample(sample_id, created.md5sum)
        # assert response.status_code == 200
        #
        # retrieved = File.from_dict(response.json)
        # assert retrieved == created