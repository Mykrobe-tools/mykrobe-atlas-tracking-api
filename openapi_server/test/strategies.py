from hashlib import md5

from hypothesis.strategies import composite, text, integers, floats, sampled_from, characters

from openapi_server.models import Event, QcResult
from openapi_server.models.file import File


def int32s():
    return integers(min_value=-2**31, max_value=2**31-1)


def int64s():
    return integers(min_value=-2**63, max_value=2**63-1)


def sample_ids():
    return text(alphabet=characters(whitelist_categories=('L', 'N')), min_size=1)


@composite
def md5s(draw):
    return md5(draw(text(min_size=1)).encode()).hexdigest()


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


@composite
def files(draw):
    return File(
        md5sum=draw(md5s()),
        filename=draw(text()),
        file_type=draw(sampled_from(['fastq', 'vcf']))
    )


@composite
def qc_results(draw):
    return QcResult(
        coverage=draw(int32s()),
        tbc=draw(text()),
        decision=draw(sampled_from(['pass', 'fail']))
    )