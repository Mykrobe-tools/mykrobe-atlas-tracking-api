from hypothesis.strategies import composite, text, integers, floats, sampled_from, characters

from openapi_server.models import Event


def sample_ids():
    return text(alphabet=characters(whitelist_categories=('L', 'N')), min_size=1)


@composite
def events(draw):
    return Event(
        command=draw(text()),
        duration=draw(integers()),
        name=draw(sampled_from(['de-contamination', 'QC', 'variant-calling', 'prediction', 'bigsi-building', 'distance-calculation'])),
        software=draw(text()),
        software_version=draw(text()),
        start_time=draw(floats())
    )
