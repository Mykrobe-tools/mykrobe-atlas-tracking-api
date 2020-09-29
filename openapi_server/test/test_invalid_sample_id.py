from pathlib import Path
from uuid import UUID

from hypothesis import settings, HealthCheck, given, assume
from pytest import fixture

from openapi_server.test.strategies import safe_strings


ENDPOINT_NAME = 'endpoint'
PARAM_NAME = 'sample_id'


def handler(sample_id):
    raise Exception('body reached')


@fixture
def app(app):
    app.add_api({
        'openapi': '3.0.0',
        'info': {
            'title': '',
            'version': ''
        },
        'paths': {
            f'/{ENDPOINT_NAME}/{{{PARAM_NAME}}}': {
                'get': {
                    'parameters': [
                        {
                            'name': PARAM_NAME,
                            'in': 'path',
                            'schema': {
                                '$ref': f'file:////{Path(__file__).parent.parent.absolute()}/openapi/openapi.yaml#/components/schemas/SampleID'
                            }
                        }
                    ],
                    'responses': {
                        '200': {
                            'description': 'ok'
                        }
                    },
                    'x-openapi-router-controller': __name__,
                    'operationId': handler.__name__
                }
            }
        }
    })
    return app


@fixture
def call_endpoint(make_request):
    def _(sample_id, *args, **kwargs):
        return make_request(f'/{ENDPOINT_NAME}/{sample_id}', 'GET', *args, **kwargs)
    return _


@settings(suppress_health_check=(HealthCheck.filter_too_much,))
@given(sample_id=safe_strings(min_size=1))
def test_invalid_sample_id(sample_id, call_endpoint):
    def is_uuid(s):
        try:
            UUID(s, version=4)
        except ValueError:
            return False
        else:
            return True
    assume(not is_uuid(sample_id))

    assert call_endpoint(sample_id).status_code == 400