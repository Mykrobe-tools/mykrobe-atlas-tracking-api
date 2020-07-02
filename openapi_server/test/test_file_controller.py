# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.error import Error  # noqa: E501
java.io.File  # noqa: E501
from openapi_server.test import BaseTestCase


class TestFileController(BaseTestCase):
    """FileController integration test stubs"""

    def test_files_md5sum_get(self):
        """Test case for files_md5sum_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/files/{md5sum}'.format(md5sum='md5sum_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_samples_id_files_get(self):
        """Test case for samples_id_files_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/samples/{id}/files'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_samples_id_files_md5sum_delete(self):
        """Test case for samples_id_files_md5sum_delete

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/samples/{id}/files/{md5sum}'.format(id='id_example', md5sum='md5sum_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_samples_id_files_md5sum_get(self):
        """Test case for samples_id_files_md5sum_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/samples/{id}/files/{md5sum}'.format(id='id_example', md5sum='md5sum_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_samples_id_files_post(self):
        """Test case for samples_id_files_post

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/samples/{id}/files'.format(id='id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
