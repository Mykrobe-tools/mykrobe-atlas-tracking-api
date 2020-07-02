# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.qc_result import QcResult  # noqa: E501
from openapi_server.test import BaseTestCase


class TestQcResultController(BaseTestCase):
    """QcResultController integration test stubs"""

    def test_samples_id_qc_result_delete(self):
        """Test case for samples_id_qc_result_delete

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/samples/{id}/qc-result'.format(id='id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_samples_id_qc_result_get(self):
        """Test case for samples_id_qc_result_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/samples/{id}/qc-result'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_samples_id_qc_result_put(self):
        """Test case for samples_id_qc_result_put

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/samples/{id}/qc-result'.format(id='id_example'),
            method='PUT',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
