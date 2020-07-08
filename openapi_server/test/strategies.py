from hypothesis.strategies import composite, text, integers, floats, sampled_from, characters

from openapi_server.models import Event


def int64s():
    return integers(min_value=-2**63, max_value=2**63-1)


def sample_ids():
    return text(alphabet=characters(whitelist_categories=('L', 'N')), min_size=1)


@composite
def events(draw, without_id=False):
    event_id = None if without_id else draw(int64s())
    return Event(
        id=event_id,
        command=draw(text()),
        duration=draw(int64s()),
        name=draw(sampled_from(['de-contamination', 'QC', 'variant-calling', 'prediction', 'bigsi-building', 'distance-calculation'])),
        software=draw(text()),
        software_version=draw(text()),
        start_time=draw(floats())
    )