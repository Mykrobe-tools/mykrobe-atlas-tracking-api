from hypothesis import given
from hypothesis.strategies import lists

from openapi_server.models import Event
from openapi_server.test.assertions import assert_equal_events, \
    assert_creating_secondary_resource_with_primary_resource, assert_listing_secondary_resources
from openapi_server.test.context_managers import managed_db
from openapi_server.test.strategies import events, sample_ids


@given(primary_pk_value=sample_ids(), other_primary_pk_value=sample_ids(), secondary_resources=lists(events(), min_size=1, unique_by=lambda x: x.id))
def test_listing_behaviours(primary_pk_value, other_primary_pk_value, secondary_resources, create_sample, create_event,
                            list_events):
    assert_listing_secondary_resources(primary_pk_value, other_primary_pk_value, secondary_resources, create_sample, create_event, list_events)


@given(primary_pk_value=sample_ids(), secondary_resource=events(without_id=True))
def test_creating_behaviours(primary_pk_value, secondary_resource, create_sample, create_event, get_event):
    assert_creating_secondary_resource_with_primary_resource(
        primary_pk_value, secondary_resource, create_primary=create_sample, create_secondary=create_event, get_secondary=get_event,
        secondary_eq_assertion=assert_equal_events, db_generated_pk=True
    )


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


@given(sample_id=sample_ids(), event=events())
def test_deleting_events_of_non_existent_samples(sample_id, event, delete_event, create_event, create_sample, delete_sample):
    with managed_db():
        create_sample(sample_id)
        create_event(sample_id, event, ensure=True)
        delete_sample(sample_id)

        response = delete_event(sample_id, event.id)
        assert response.status_code == 404


@given(sample_id=sample_ids(), event=events())
def test_deleting_non_existent_events(sample_id, event, delete_event, create_sample):
    with managed_db():
        create_sample(sample_id)
        response = delete_event(sample_id, event.id)
        assert response.status_code == 404


@given(sample_id=sample_ids(), event=events())
def test_deleting_events(sample_id, event, delete_event, create_event, create_sample, get_event):
    with managed_db():
        create_sample(sample_id)
        create_event(sample_id, event, ensure=True)

        response = delete_event(sample_id, event.id)
        assert response.status_code == 204

        response = get_event(sample_id, event.id)
        assert response.status_code == 404
