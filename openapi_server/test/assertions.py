import math

from pytest import approx

from openapi_server.models import Event


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
