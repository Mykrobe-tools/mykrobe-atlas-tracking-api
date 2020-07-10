# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Event(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None, software=None, software_version=None, start_time=None, duration=None, command=None):  # noqa: E501
        """Event - a model defined in OpenAPI

        :param id: The id of this Event.  # noqa: E501
        :type id: int
        :param name: The name of this Event.  # noqa: E501
        :type name: str
        :param software: The software of this Event.  # noqa: E501
        :type software: str
        :param software_version: The software_version of this Event.  # noqa: E501
        :type software_version: str
        :param start_time: The start_time of this Event.  # noqa: E501
        :type start_time: float
        :param duration: The duration of this Event.  # noqa: E501
        :type duration: int
        :param command: The command of this Event.  # noqa: E501
        :type command: str
        """
        self.openapi_types = {
            'id': int,
            'name': str,
            'software': str,
            'software_version': str,
            'start_time': float,
            'duration': int,
            'command': str
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'software': 'software',
            'software_version': 'software-version',
            'start_time': 'start-time',
            'duration': 'duration',
            'command': 'command'
        }

        self._id = id
        self._name = name
        self._software = software
        self._software_version = software_version
        self._start_time = start_time
        self._duration = duration
        self._command = command

    @classmethod
    def from_dict(cls, dikt) -> 'Event':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Event of this Event.  # noqa: E501
        :rtype: Event
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Event.


        :return: The id of this Event.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Event.


        :param id: The id of this Event.
        :type id: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Event.


        :return: The name of this Event.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Event.


        :param name: The name of this Event.
        :type name: str
        """
        allowed_values = ["de-contamination", "QC", "variant-calling", "prediction", "bigsi-building", "distance-calculation"]  # noqa: E501
        if name not in allowed_values:
            raise ValueError(
                "Invalid value for `name` ({0}), must be one of {1}"
                .format(name, allowed_values)
            )

        self._name = name

    @property
    def software(self):
        """Gets the software of this Event.


        :return: The software of this Event.
        :rtype: str
        """
        return self._software

    @software.setter
    def software(self, software):
        """Sets the software of this Event.


        :param software: The software of this Event.
        :type software: str
        """
        if software is None:
            raise ValueError("Invalid value for `software`, must not be `None`")  # noqa: E501

        self._software = software

    @property
    def software_version(self):
        """Gets the software_version of this Event.


        :return: The software_version of this Event.
        :rtype: str
        """
        return self._software_version

    @software_version.setter
    def software_version(self, software_version):
        """Sets the software_version of this Event.


        :param software_version: The software_version of this Event.
        :type software_version: str
        """
        if software_version is None:
            raise ValueError("Invalid value for `software_version`, must not be `None`")  # noqa: E501

        self._software_version = software_version

    @property
    def start_time(self):
        """Gets the start_time of this Event.


        :return: The start_time of this Event.
        :rtype: float
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this Event.


        :param start_time: The start_time of this Event.
        :type start_time: float
        """
        if start_time is None:
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

    @property
    def duration(self):
        """Gets the duration of this Event.


        :return: The duration of this Event.
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this Event.


        :param duration: The duration of this Event.
        :type duration: int
        """
        if duration is None:
            raise ValueError("Invalid value for `duration`, must not be `None`")  # noqa: E501

        self._duration = duration

    @property
    def command(self):
        """Gets the command of this Event.


        :return: The command of this Event.
        :rtype: str
        """
        return self._command

    @command.setter
    def command(self, command):
        """Sets the command of this Event.


        :param command: The command of this Event.
        :type command: str
        """
        if command is None:
            raise ValueError("Invalid value for `command`, must not be `None`")  # noqa: E501

        self._command = command
