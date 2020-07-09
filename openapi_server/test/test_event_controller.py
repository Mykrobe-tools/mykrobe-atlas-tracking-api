import random

from hypothesis import given, assume
from hypothesis.strategies import lists

from openapi_server.models import Event
from openapi_server.test.assertions import assert_equal_events, assert_equal_lists
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import events, sample_ids


@given(sample_id=sample_ids())
def test_listing_events_with_non_existent_samples(sample_id, list_event):
    response = list_event(sample_id)
    assert response.status_code == 404


@given(sample_id=sample_ids(), event_list=lists(events(), min_size=1, unique_by=lambda x: x.id), other_sample_id=sample_ids())
def test_listing_events(sample_id, event_list, other_sample_id, list_event, create_sample, create_event):
    assume(sample_id != other_sample_id)

    associated_events = random.sample(event_list, random.randrange(0, len(event_list)))

    with managed_db():
        create_sample(sample_id)
        create_sample(other_sample_id)

        for event in event_list:
            if event in associated_events:
                create_event(sample_id, event, ensure=True)
            else:
                create_event(other_sample_id, event, ensure=True)

        response = list_event(sample_id)
        assert response.status_code == 200

        listed = [Event.from_dict(x) for x in response.json]
        assert_equal_lists(listed, associated_events)


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
