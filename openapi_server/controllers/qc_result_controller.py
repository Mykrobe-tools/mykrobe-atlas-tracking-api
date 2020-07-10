import connexion
import six

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.qc_result import QcResult  # noqa: E501
from openapi_server import util


def samples_id_qc_result_delete(id):  # noqa: E501
    """samples_id_qc_result_delete

    Delete the QC result associated with a sample with {id}. # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def samples_id_qc_result_get(id):  # noqa: E501
    """samples_id_qc_result_get

    Return the QC result associated with a sample. # noqa: E501

    :param id: 
    :type id: str

    :rtype: QcResult
    """
    return 'do some magic!'


def samples_id_qc_result_put(id, qc_result):  # noqa: E501
    """samples_id_qc_result_put

    Add or replace new QC result associated with a sample. # noqa: E501

    :param id: 
    :type id: str
    :param qc_result: QC result to be added
    :type qc_result: dict | bytes

    :rtype: QcResult
    """
    if connexion.request.is_json:
        qc_result = QcResult.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
