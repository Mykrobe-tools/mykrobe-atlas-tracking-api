from hypothesis import given

from openapi_server.test.assertions import assert_resource_created
from openapi_server.test.strategies import events, sample_ids


@given(event=events(), sample_id=sample_ids())
def test_create_an_event_associated_with_an_existing_sample(event, sample_id, client):
    response = client.post(f'/api/v1/samples/{sample_id}/events', json=event)

    assert_resource_created(response, event)
