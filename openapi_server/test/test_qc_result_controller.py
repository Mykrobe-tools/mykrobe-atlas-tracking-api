from hypothesis import given

from openapi_server.models import QcResult
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import sample_ids, qc_results


@given(sample_id=sample_ids(), qc_result=qc_results())
def test_add_or_update_qc_result_of_non_existent_sample(sample_id, qc_result, add_or_replace_qc_result):
    response = add_or_replace_qc_result(sample_id, qc_result)
    assert response.status_code == 404, response.data.decode()


@given(sample_id=sample_ids(), qc_result=qc_results())
def test_add_qc_result(sample_id, qc_result, create_sample_in_db, add_or_replace_qc_result, get_qc_result, get_resource):
    with managed_db():
        create_sample_in_db(sample_id)

        response = add_or_replace_qc_result(sample_id, qc_result)
        added = QcResult.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert added == qc_result

        from_location_header = QcResult.from_dict(get_resource(response.location, ensure=True).json)
        assert added == from_location_header

        response = get_qc_result(sample_id)
        retrieved = QcResult.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert retrieved == added


@given(sample_id=sample_ids(), original=qc_results(), new=qc_results())
def test_replace_qc_result(sample_id, original, new, create_sample_in_db, add_or_replace_qc_result, get_qc_result, get_resource):
    with managed_db():
        create_sample_in_db(sample_id)
        add_or_replace_qc_result(sample_id, original, ensure=True)

        response = add_or_replace_qc_result(sample_id, new)
        updated = QcResult.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert updated == new

        from_location_header = QcResult.from_dict(get_resource(response.location, ensure=True).json)
        assert updated == from_location_header

        response = get_qc_result(sample_id)
        retrieved = QcResult.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert retrieved == updated


@given(sample_id=sample_ids())
def test_getting_qc_results_of_non_existent_samples(sample_id, get_qc_result):
    assert get_qc_result(sample_id).status_code == 404


@given(sample_id=sample_ids())
def test_getting_non_existent_qc_results(sample_id, create_sample_in_db, get_qc_result):
    with managed_db():
        create_sample_in_db(sample_id)
        assert get_qc_result(sample_id).status_code == 404


@given(sample_id=sample_ids(), qc_result=qc_results())
def test_getting_qc_results(sample_id, qc_result, create_sample_in_db, add_or_replace_qc_result, get_qc_result):
    with managed_db():
        create_sample_in_db(sample_id)
        add_or_replace_qc_result(sample_id, qc_result, ensure=True)

        response = get_qc_result(sample_id)
        retrieved = QcResult.from_dict(response.json)

        assert response.status_code == 200, response.data.decode()
        assert retrieved == qc_result


@given(sample_id=sample_ids())
def test_deleting_qc_result_of_non_existent_samples(sample_id, delete_qc_result):
    response = delete_qc_result(sample_id)
    assert response.status_code == 404


@given(sample_id=sample_ids())
def test_deleting_non_existent_qc_results(sample_id, create_sample_in_db, delete_qc_result):
    with managed_db():
        create_sample_in_db(sample_id)
        response = delete_qc_result(sample_id)
        assert response.status_code == 404


@given(sample_id=sample_ids(), qc_result=qc_results())
def test_deleting_files(sample_id, qc_result, create_sample_in_db, add_or_replace_qc_result, delete_qc_result, get_qc_result):
    with managed_db():
        create_sample_in_db(sample_id)
        add_or_replace_qc_result(sample_id, qc_result, ensure=True)

        response = delete_qc_result(sample_id)
        assert response.status_code == 204

        response = get_qc_result(sample_id)
        assert response.status_code == 404