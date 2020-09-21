from hashlib import md5

from hypothesis.strategies import composite, text, integers, floats, sampled_from, characters, uuids

from openapi_server.models import Event, QcResult, Status, Sample
from openapi_server.models.file import File


def int32s():
    return integers(min_value=-2**31, max_value=2**31-1)


def safe_strings(*args, **kwargs):
    return text(alphabet=characters(whitelist_categories=('L', 'N')), *args, **kwargs)


@composite
def samples(draw):
    return Sample(
        experiment_id=draw(safe_strings(min_size=1)),
        isolate_id=draw(safe_strings(min_size=1))
    )


def sample_ids():
    return uuids()


@composite
def md5s(draw):
    return md5(draw(text(min_size=1)).encode()).hexdigest()


@composite
def events(draw, without_id=False):
    event_id = None if without_id else draw(int32s())
    return Event(
        id=event_id,
        command=draw(safe_strings()),
        duration=draw(int32s()),
        name=draw(sampled_from(['de-contamination', 'QC', 'variant-calling', 'prediction', 'bigsi-building', 'distance-calculation'])),
        software=draw(safe_strings()),
        software_version=draw(safe_strings()),
        start_time=draw(floats())
    )


@composite
def files(draw):
    return File(
        md5sum=draw(md5s()),
        filename=draw(safe_strings()),
        file_type=draw(sampled_from(['fastq', 'vcf']))
    )


@composite
def qc_results(draw):
    return QcResult(
        coverage=draw(floats(allow_nan=False)),
        tbc=draw(safe_strings()),
        decision=draw(sampled_from(['passed', 'failed']))
    )


@composite
def statuses(draw):
    processing_statuses = ['pending', 'started', 'complete', 'failed']
    return Status(
        de_contamination=draw(sampled_from(processing_statuses)),
        qc=draw(sampled_from(processing_statuses)),
        variant_calling=draw(sampled_from(processing_statuses)),
        prediction=draw(sampled_from(processing_statuses)),
        bigsi_building=draw(sampled_from(processing_statuses)),
        distance_calculation=draw(sampled_from(processing_statuses)),
        stage=draw(sampled_from(["accepted", "qc-failed", "live", "deprecated"]))
    )