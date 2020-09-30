import uuid

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from openapi_server import models
from openapi_server.db import db
from openapi_server.models.base_model_ import Model

# Create a PostgreSQL UUID column
# as_uuid = True: In Python, this field will have the `uuid` type (instead of `str`)

UUID_TYPE = UUID(as_uuid=True)


class APIModelMixin:
    @classmethod
    def from_model(cls, model: Model) -> db.Model:
        props = {p: getattr(model, p) for p in cls.api_model_properties()}
        return cls(**props)

    def to_model(self) -> Model:
        props = {p: getattr(self, p) for p in self.api_model_properties()}
        return self.api_model_class(**props)

    @classmethod
    def api_model_properties(cls):
        return [p for p in dir(cls.api_model_class) if isinstance(getattr(cls.api_model_class, p), property)]


class Event(APIModelMixin, db.Model):
    id = Column(Integer, primary_key=True)
    command = Column(String)
    duration = Column(Integer)
    name = Column(String)
    software = Column(String)
    software_version = Column(String)
    start_time = Column(Float)

    sample_id = Column(UUID_TYPE, ForeignKey('sample.id'))

    api_model_class = models.Event


class File(APIModelMixin, db.Model):
    md5sum = Column(String, primary_key=True)
    filename = Column(String)
    file_type = Column(String)

    sample_id = Column(UUID_TYPE, ForeignKey('sample.id'))

    api_model_class = models.File


class QcResult(APIModelMixin, db.Model):
    id = Column(Integer, primary_key=True)
    coverage = Column(Float)
    number_of_het_snps = Column(Integer)
    decision = Column(String)

    sample_id = Column(UUID_TYPE, ForeignKey('sample.id'))

    api_model_class = models.QcResult


class Status(APIModelMixin, db.Model):
    id = Column(Integer, primary_key=True)
    de_contamination = Column(String)
    qc = Column(String)
    variant_calling = Column(String)
    prediction = Column(String)
    bigsi_building = Column(String)
    distance_calculation = Column(String)
    stage = Column(String)

    sample_id = Column(UUID_TYPE, ForeignKey('sample.id'))

    api_model_class = models.Status


class Sample(APIModelMixin, db.Model):
    experiment_id = Column(String, unique=True)
    isolate_id = Column(String, unique=True)

    id = Column(UUID_TYPE, primary_key=True, default=uuid.uuid4)

    events = db.relationship(Event, backref='sample')
    files = db.relationship(File, backref='sample')
    qc_result = db.relationship(QcResult, backref='sample', uselist=False)
    status = db.relationship(Status, backref='sample', uselist=False)

    api_model_class = models.Sample
