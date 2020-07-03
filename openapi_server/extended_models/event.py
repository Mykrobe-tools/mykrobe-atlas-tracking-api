from typing import NewType, Union, Literal

from openapi_server import models, orm

EventName = NewType('EventName', Union[
    Literal['de-contamination'],
    Literal['QC'],
    Literal['variant-calling'],
    Literal['prediction'],
    Literal['bigsi-building'],
    Literal['distance-calculation']
])


class Event(models.Event):
    @classmethod
    def create(cls, command: str, duration: int, name: EventName, software: str, software_version: str, start_time: float):
        orm.Event

