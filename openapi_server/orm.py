from sqlalchemy import Column, String, Integer, Float, ForeignKey

from openapi_server import models
from openapi_server.db import db
from openapi_server.models.base_model_ import Model


# class CRUDMixin:
#     @classmethod
#     def create(cls, model: Model) -> db.Model:
#         inst = cls.from_model(model)
#         inst.create()
#         return inst
#
#     def create(self):
#         db.session.add(self)
#         db.session.commit()


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

    sample_id = Column(String, ForeignKey('sample.id'))

    api_model_class = models.Event


class Sample(db.Model):
    id = Column(String, primary_key=True)
    events = db.relationship(Event, backref='sample')
