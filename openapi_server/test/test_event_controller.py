from hypothesis import given

from openapi_server.models import Event
from openapi_server.test.assertions import assert_equal_events
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import events, sample_ids


@given(sample_id=sample_ids(), event=events())
def test_creating_events_with_non_existent_samples(sample_id, event, create_event):
    response = create_event(sample_id, event)
    assert response.status_code == 404


@given(sample_id=sample_ids(), event=events(without_id=True))
def test_creating_events(sample_id, event, create_event, get_event, create_sample):
    with managed_db():
        create_sample(sample_id)

        response = create_event(sample_id, event)
        assert response.status_code == 201
        event.id = response.json['id']

        response = get_event(sample_id, event.id)
        assert response.status_code == 200

        created = Event.from_dict(response.json)
        assert_equal_events(created, event)


@given(sample_id=sample_ids(), event=events())
def test_getting_events_of_non_existent_samples(sample_id, event, get_event, create_event, create_sample, delete_sample):
    with managed_db():
        create_sample(sample_id)
        create_event(sample_id, event, ensure=True)
        delete_sample(sample_id)

        response = get_event(sample_id, event.id)
        assert response.status_code == 404


@given(sample_id=sample_ids(), event=events())
def test_getting_non_existent_events(sample_id, event, get_event, create_sample):
    with managed_db():
        create_sample(sample_id)
        response = get_event(sample_id, event.id)
        assert response.status_code == 404


@given(sample_id=sample_ids(), event=events())
def test_getting_events(sample_id, event, get_event, create_event, create_sample):
    with managed_db():
        create_sample(sample_id)
        create_event(sample_id, event, ensure=True)

        response = get_event(sample_id, event.id)
        assert response.status_code == 200

        created = Event.from_dict(response.json)
        assert_equal_events(created, event)
