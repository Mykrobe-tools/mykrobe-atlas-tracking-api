# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class File(Model):
    """NOTE: This class is COPIED FROM A GENERATED MODEL because OpenAPI Generator (https://openapi-generator.tech) couldn't generate the model (unknown reason).

    Do not edit the class manually ANY FURTHER.
    """

    def __init__(self, md5sum=None, filename=None, file_type=None):  # noqa: E501
        """File - a model defined in OpenAPI

        :param md5sum: The md5sum of this File.  # noqa: E501
        :type md5sum: str
        :param filename: The filename of this File.  # noqa: E501
        :type filename: str
        :param file_type: The file_type of this Event.  # noqa: E501
        :type file_type: str
        """
        self.openapi_types = {
            'md5sum': str,
            'filename': str,
            'file_type': str
        }

        self.attribute_map = {
            'md5sum': 'md5sum',
            'filename': 'filename',
            'file_type': 'file-type'
        }

        self._md5sum = md5sum
        self._filename = filename
        self._file_type = file_type

    @classmethod
    def from_dict(cls, dikt) -> 'File':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The File of this Event.  # noqa: E501
        :rtype: File
        """
        return util.deserialize_model(dikt, cls)

    @property
    def md5sum(self):
        """Gets the md5sum of this File.


        :return: The md5sum of this File.
        :rtype: str
        """
        return self._md5sum

    @md5sum.setter
    def md5sum(self, md5sum):
        """Sets the md5sum of this File.


        :param md5sum: The md5sum of this File.
        :type md5sum: str
        """

        self._md5sum = md5sum

    @property
    def filename(self):
        """Gets the filename of this File.


        :return: The filename of this File.
        :rtype: str
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """Sets the filename of this File.


        :param filename: The filename of this File.
        :type filename: str
        """
        self._filename = filename

    @property
    def file_type(self):
        """Gets the file_type of this File.


        :return: The file_type of this File.
        :rtype: str
        """
        return self._file_type

    @file_type.setter
    def file_type(self, file_type):
        """Sets the file_type of this File.


        :param file_type: The file_type of this File.
        :type file_type: str
        """
        allowed_values = ["fastq", "vcf"]  # noqa: E501
        if file_type not in allowed_values:
            raise ValueError(
                "Invalid value for `file_type` ({0}), must be one of {1}"
                .format(file_type, allowed_values)
            )

        self._file_type = file_type
