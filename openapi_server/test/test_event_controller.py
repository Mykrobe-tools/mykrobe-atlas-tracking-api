# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.event import Event  # noqa: E501
from openapi_server.test import BaseTestCase


class TestEventController(BaseTestCase):
    """EventController integration test stubs"""

    def test_samples_id_events_event_id_delete(self):
        """Test case for samples_id_events_event_id_delete

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/samples/{id}/events/{event_id}'.format(id='id_example', event_id='event_id_example'),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_samples_id_events_event_id_get(self):
        """Test case for samples_id_events_event_id_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/samples/{id}/events/{event_id}'.format(id='id_example', event_id='event_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_samples_id_events_get(self):
        """Test case for samples_id_events_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/samples/{id}/events'.format(id='id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_samples_id_events_post(self):
        """Test case for samples_id_events_post

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/samples/{id}/events'.format(id='id_example'),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
