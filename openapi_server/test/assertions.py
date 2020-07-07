import math

from pytest import approx


def assert_float_representations_equal(a, b):
    if not a or math.isnan(a):
        assert not b or math.isnan(b)
    elif not b or math.isnan(b):
        assert not a or math.isnan(a)
    else:
        assert a == approx(b)


def assert_equal_events(a, b):
    assert a.id == b.id
    assert a.command == b.command
    assert a.duration == b.duration
    assert a.name == b.name
    assert a.software == b.software
    assert a.software_version == b.software_version
    assert_float_representations_equal(a.start_time, b.start_time)
