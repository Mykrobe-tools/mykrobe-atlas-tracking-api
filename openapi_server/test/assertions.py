import math

from pytest import approx

from openapi_server.models import Event
from openapi_server.test.context_managers import managed_db


def assert_float_representations_equal(a, b):
    if not a or math.isnan(a):
        assert not b or math.isnan(b)
    elif not b or math.isnan(b):
        assert not a or math.isnan(a)
    else:
        assert a == approx(b)


def assert_equal_lists(a, b):
    assert len(a) == len(b)
    for x in a:
        if isinstance(x, Event):
            xb = [y for y in b if y.id == x.id][0]
            assert_equal_events(x, xb)
        else:
            assert x in b


def assert_equal_events(a, b, compare_id=True):
    if compare_id:
        assert a.id == b.id
    assert a.command == b.command
    assert a.duration == b.duration
    assert a.name == b.name
    assert a.software == b.software
    assert a.software_version == b.software_version
    assert_float_representations_equal(a.start_time, b.start_time)


def assert_equal_resources(a, b, compare_id=True):
    assert a == b


def assert_creating_secondary_resource_with_primary_resource(
        primary_pk_value, secondary_resource, create_primary, create_secondary, get_secondary, strict_lookup=True, secondary_pk_name='id', secondary_eq_assertion=assert_equal_resources,
        db_generated_pk=False
):
    response = create_secondary(primary_pk_value, secondary_resource)
    assert response.status_code == 404

    with managed_db():
        create_primary(primary_pk_value)

        response = create_secondary(primary_pk_value, secondary_resource)
        assert response.status_code == 201

        created = type(secondary_resource).from_dict(response.json)
        secondary_eq_assertion(created, secondary_resource, compare_id=False if db_generated_pk else True)

        secondary_pk_value = getattr(created, secondary_pk_name)
        if strict_lookup:
            response = get_secondary(primary_pk_value, secondary_pk_value)
        else:
            response = get_secondary(secondary_pk_value)
        assert response.status_code == 200

        retrieved = type(secondary_resource).from_dict(response.json)
        secondary_eq_assertion(retrieved, created)

        if not db_generated_pk:
            response = create_secondary(primary_pk_value, secondary_resource)
            assert response.status_code == 409