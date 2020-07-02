def test_create_an_event_associated_with_an_existing_sample(client):
    sample_id = '0'

    response = client.post(f'/api/v1/samples/{sample_id}/events')

    assert response.status_code == 201, response.data.decode()
