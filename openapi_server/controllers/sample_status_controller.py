import connexion
import six

from openapi_server.db import db
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.status import Status  # noqa: E501
from openapi_server import util, orm


def samples_id_status_delete(id):  # noqa: E501
    """samples_id_status_delete

    Delete the status associated with a sample with {id}. # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """

    sample = orm.Sample.query.get(id)
    if not sample or not sample.status:
        return Error(404, 'Not found'), 404

    db.session.delete(sample.status)
    db.session.commit()

    return '', 204


def samples_id_status_get(id):  # noqa: E501
    """samples_id_status_get

    Return the status associated with a sample. # noqa: E501

    :param id: 
    :type id: str

    :rtype: Status
    """

    sample = orm.Sample.query.get(id)
    if not sample or not sample.status:
        return Error(404, 'Not found'), 404

    return sample.status.to_model(), 200


def samples_id_status_patch(id, status=None):  # noqa: E501
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

    sample = orm.Sample.query.get(id)
    if not sample:
        return Error(404, 'Not found'), 404

    for prop in sample.status.api_model_properties():
        if (new_value := getattr(status, prop)) is not None:
            setattr(sample.status, prop, new_value)

    db.session.commit()

    return sample.status.to_model(), 200


def samples_id_status_put(id, status=None):  # noqa: E501
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

    sample = orm.Sample.query.get(id)
    if not sample:
        return Error(404, 'Not found'), 404

    inst = orm.Status.from_model(status)
    inst.sample_id = sample.id

    if sample.status:
        sample.status = inst
    else:
        db.session.add(inst)
    db.session.commit()

    return inst.to_model(), 200
