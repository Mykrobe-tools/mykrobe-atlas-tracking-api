# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.test import BaseTestCase


class TestSampleController(BaseTestCase):
    """SampleController integration test stubs"""

    def test_samples_id_head(self):
        """Test case for samples_id_head

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/samples/{id}'.format(id='id_example'),
            method='HEAD',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
