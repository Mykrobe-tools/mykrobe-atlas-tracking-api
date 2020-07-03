def assert_resource_created(response, requested_resource, many=False):
    assert response.status_code == 201, response.data.decode()

    resource_class = type(requested_resource)
    if not many:
        responded_resource = resource_class.from_dict(response.json)
    else:
        responded_resource = [resource_class.from_dict(x) for x in response.json]

    assert responded_resource == requested_resource
