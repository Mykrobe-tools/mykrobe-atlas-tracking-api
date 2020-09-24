import connexion
from sqlalchemy.exc import IntegrityError

from openapi_server import orm
from openapi_server.db import db
from openapi_server.input_validators import validate_sample_id
from openapi_server.models import Sample
from openapi_server.models.error import Error  # noqa: E501


def samples_id_get(id):  # noqa: E501
    """samples_id_get

    Return a sample by its ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: Sample
    """

    validate_sample_id(id)

    resource = orm.Sample.query.get(id)
    if not resource:
        return Error(404, 'Not found'), 404

    return resource.to_model(), 200


def samples_id_head(id):  # noqa: E501
    """samples_id_head

    Return if a sample with {id} exists. # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """

    validate_sample_id(id)

    resource = orm.Sample.query.get(id)
    if not resource:
        return Error(404, 'Not found'), 404

    return '', 200


def samples_post(sample=None):  # noqa: E501
    """samples_post

    Add a new sample. # noqa: E501

    :param sample: Sample to be added
    :type sample: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        sample = Sample.from_dict(connexion.request.get_json())  # noqa: E501

    inst = orm.Sample.from_model(sample)

    db.session.add(inst)
    try:
        db.session.commit()
    except IntegrityError:
        return Error(409, 'Already existed'), 409
    else:
        return inst.to_model(), 201, {'location': f'samples/{inst.id}'}