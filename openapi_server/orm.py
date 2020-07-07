from sqlalchemy import Column, String, Integer, Float

from openapi_server import models
from openapi_server.db import db
from openapi_server.models.base_model_ import Model


class CRUDMixin:
    @classmethod
    def create(cls, model: Model) -> db.Model:
        inst = cls.from_model(model)

        db.session.add(inst)
        db.session.commit()

        return inst

    @classmethod
    def from_model(cls, model: Model) -> db.Model:
        attrs = {k: getattr(model, k) for k in cls.api_model_props()}
        return cls(**attrs)

    def to_model(self) -> Model:
        attrs = {k: getattr(self, k) for k in self.api_model_props()}
        return self.api_model(**attrs)

    @classmethod
    def api_model_props(cls):
        return [p for p in dir(cls.api_model) if isinstance(getattr(cls.api_model, p), property)]


class Event(CRUDMixin, db.Model):
    id = Column(Integer, primary_key=True)
    command = Column(String)
    duration = Column(Integer)
    name = Column(String)
    software = Column(String)
    software_version = Column(String)
    start_time = Column(Float)

    api_model = models.Event


class Sample(db.Model):
    id = Column(String, primary_key=True)
