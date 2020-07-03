from sqlalchemy import Column, String, Integer, Float

from openapi_server.db import get_db

db = get_db()


class Event(db.Model):
    id = Column(Integer, primary_key=True)
    command = Column(String)
    duration = Column(Integer)
    name = Column(String)
    software = Column(String)
    software_version = Column(String)
    start_time = Column(Float)


class Sample(db.Model):
    id = Column(String, primary_key=True)
