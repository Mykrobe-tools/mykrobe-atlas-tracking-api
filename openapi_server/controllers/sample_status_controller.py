import connexion
import six

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.status import Status  # noqa: E501
from openapi_server import util


def samples_id_status_delete(id):  # noqa: E501
    """samples_id_status_delete

    Delete the status associated with a sample with {id}. # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def samples_id_status_get(id):  # noqa: E501
    """samples_id_status_get

    Return the status associated with a sample. # noqa: E501

    :param id: 
    :type id: str

    :rtype: Status
    """
    return 'do some magic!'


def samples_id_status_patch(id, status):  # noqa: E501
    """samples_id_status_patch

    Update status associated with a sample with new data. # noqa: E501

    :param id: 
    :type id: str
    :param status: Status to be added
    :type status: dict | bytes

    :rtype: Status
    """
    if connexion.request.is_json:
        status = Status.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def samples_id_status_put(id, status):  # noqa: E501
    """samples_id_status_put

    Add or replace new status associated with a sample. # noqa: E501

    :param id: 
    :type id: str
    :param status: Status to be added.
    :type status: dict | bytes

    :rtype: Status
    """
    if connexion.request.is_json:
        status = Status.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
