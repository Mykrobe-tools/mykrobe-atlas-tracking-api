import random

from openapi_server.test.assertions import assert_equal_resources, assert_equal_lists
from openapi_server.test.context_managers import managed_db


def check_creating_secondary_resource_scenarios(
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


def check_listing_secondary_resources_scenarios(primary_pk_values, secondary_resources, create_primary, create_secondary, list_secondary):
    primary_pk_value, other_primary_pk_value = primary_pk_values

    response = list_secondary(primary_pk_value)
    assert response.status_code == 404

    associated_secondary_resources = random.sample(secondary_resources, random.randrange(0, len(secondary_resources)))

    with managed_db():
        create_primary(primary_pk_value)
        create_primary(other_primary_pk_value)

        for secondary in secondary_resources:
            if secondary in associated_secondary_resources:
                create_secondary(primary_pk_value, secondary, ensure=True)
            else:
                create_secondary(other_primary_pk_value, secondary, ensure=True)

        response = list_secondary(primary_pk_value)
        assert response.status_code == 200

        listed = [type(secondary_resources[0]).from_dict(x) for x in response.json]
        assert_equal_lists(listed, associated_secondary_resources)


def check_getting_secondary_resource_of_non_existent_primary_resource(
        primary_resource, secondary_resource, get_secondary_resource, create_secondary_resource, create_primary_resource, delete_primary_resource,
        secondary_pk_name='id'):
    with managed_db():
        create_primary_resource(primary_resource)
        create_secondary_resource(primary_resource, secondary_resource, ensure=True)
        delete_primary_resource(primary_resource)

        response = get_secondary_resource(primary_resource, getattr(secondary_resource, secondary_pk_name))
        assert response.status_code == 404


def check_getting_non_existent_secondary_resource(primary_resource, secondary_resource, get_secondary_resource, create_primary_resource,
                                                  secondary_pk_name='id'):
    with managed_db():
        create_primary_resource(primary_resource)
        response = get_secondary_resource(primary_resource, getattr(secondary_resource, secondary_pk_name))
        assert response.status_code == 404


def check_getting_secondary_resource(primary_resource, secondary_resource, get_secondary_resource, create_secondary_resource, create_primary_resource,
                                     secondary_eq_assertion=assert_equal_resources, secondary_pk_name='id'):
    with managed_db():
        create_primary_resource(primary_resource)
        create_secondary_resource(primary_resource, secondary_resource, ensure=True)

        response = get_secondary_resource(primary_resource, getattr(secondary_resource, secondary_pk_name))
        assert response.status_code == 200

        created = type(secondary_resource).from_dict(response.json)
        secondary_eq_assertion(created, secondary_resource)