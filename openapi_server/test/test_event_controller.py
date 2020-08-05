import random

from hypothesis import given
from hypothesis.strategies import lists, sets

from openapi_server.models import Event
from openapi_server.test.assertions import assert_equal_events, assert_equal_lists
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import events, sample_ids


@given(sample_id=sample_ids())
def test_listing_events_of_non_existent_sample(sample_id, list_events):
    response = list_events(sample_id)
    assert response.status_code == 404


@given(sample_id_pair=sets(sample_ids(), min_size=2, max_size=2),
       event_list=lists(events(), min_size=1, unique_by=lambda x: x.id))
def test_listing_events(sample_id_pair, event_list, create_sample, add_event,
                        list_events):
    sample_id, other_sample_id = sample_id_pair
    associated_events = random.sample(event_list, random.randrange(0, len(event_list)))

    with managed_db():
        create_sample(sample_id)
        create_sample(other_sample_id)

        for event in event_list:
            if event in associated_events:
                add_event(sample_id, event, ensure=True)
            else:
                add_event(other_sample_id, event, ensure=True)

        response = list_events(sample_id)
        assert response.status_code == 200

        listed = [Event.from_dict(x) for x in response.json]
        assert_equal_lists(listed, associated_events)


@given(sample_id=sample_ids(), event=events(without_id=True))
def test_adding_events_to_non_existent_sample(sample_id, event, add_event):
    response = add_event(sample_id, event)
    assert response.status_code == 404


@given(sample_id=sample_ids(), event=events(without_id=True))
def test_adding_events(sample_id, event, create_sample, add_event, get_event):
    with managed_db():
        create_sample(sample_id)

        response = add_event(sample_id, event)
        assert response.status_code == 201

        created = Event.from_dict(response.json)
        assert_equal_events(created, event, compare_id=False)

        response = get_event(sample_id, created.id)
        assert response.status_code == 200

        retrieved = Event.from_dict(response.json)
        assert_equal_events(retrieved, created)


@given(sample_id=sample_ids(), event=events())
def test_getting_events_of_non_existent_samples(sample_id, event, get_event, add_event, create_sample, delete_sample):
    with managed_db():
        create_sample(sample_id)
        add_event(sample_id, event, ensure=True)
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
def test_getting_events(sample_id, event, get_event, add_event, create_sample):
    with managed_db():
        create_sample(sample_id)
        add_event(sample_id, event, ensure=True)

        response = get_event(sample_id, event.id)
        assert response.status_code == 200

        created = type(event).from_dict(response.json)
        assert_equal_events(created, event)


@given(sample_id=sample_ids(), event=events())
def test_deleting_events_of_non_existent_samples(sample_id, event, delete_event):
    with managed_db():
        response = delete_event(sample_id, event.id)
        assert response.status_code == 404


@given(sample_id=sample_ids(), event=events())
def test_deleting_non_existent_events(sample_id, event, delete_event, create_sample):
    with managed_db():
        create_sample(sample_id)
        response = delete_event(sample_id, event.id)
        assert response.status_code == 404


@given(sample_id=sample_ids(), event=events())
def test_deleting_events(sample_id, event, delete_event, add_event, create_sample, get_event):
    with managed_db():
        create_sample(sample_id)
        add_event(sample_id, event, ensure=True)

        response = delete_event(sample_id, event.id)
        assert response.status_code == 204

        response = get_event(sample_id, event.id)
        assert response.status_code == 404
