import connexion

from openapi_server import orm
from openapi_server.factories.db import db
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.qc_result import QcResult  # noqa: E501


def samples_id_qc_result_delete(id):  # noqa: E501
    """samples_id_qc_result_delete

    Delete the QC result associated with a sample with {id}. # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """

    sample = orm.Sample.query.get(id)
    if not sample or not sample.qc_result:
        return Error(404, 'Not found'), 404

    db.session.delete(sample.qc_result)
    db.session.commit()

    return '', 204


def samples_id_qc_result_get(id):  # noqa: E501
    """samples_id_qc_result_get

    Return the QC result associated with a sample. # noqa: E501

    :param id: 
    :type id: str

    :rtype: QcResult
    """

    sample = orm.Sample.query.get(id)
    if not sample or not sample.qc_result:
        return Error(404, 'Not found'), 404

    return sample.qc_result.to_model(), 200


def samples_id_qc_result_put(id, qc_result=None):  # noqa: E501
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

    sample = orm.Sample.query.get(id)
    if not sample:
        return Error(404, 'Not found'), 404

    inst = orm.QcResult.from_model(qc_result)
    inst.sample_id = sample.id

    if sample.qc_result:
        sample.qc_result = inst
    else:
        db.session.add(inst)
    db.session.commit()

    return inst.to_model(), 200, {'location': ''}
