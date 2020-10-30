import connexion
from sqlalchemy.exc import IntegrityError

from openapi_server import orm
from openapi_server.db import db
from openapi_server.models import Sample
from openapi_server.models.error import Error  # noqa: E501


def samples_get(experiment_id=None, isolate_id=None):  # noqa: E501
    """samples_get

    Return a list of samples based on filtering parameters. # noqa: E501

    :param experiment_id:
    :type experiment_id: str
    :param isolate_id:
    :type isolate_id: str

    :rtype: List[Sample]
    """

    filters = []

    if experiment_id is not None:
        filters.append(orm.Sample.experiment_id == experiment_id)  # noqa: E711
    if isolate_id is not None:
        filters.append(orm.Sample.isolate_id == isolate_id)  # noqa: E711

    filtered = orm.Sample.query.filter(*filters)

    return [x.to_model() for x in filtered.all()]


def samples_id_get(id):  # noqa: E501
    """samples_id_get

    Return a sample by its ID. # noqa: E501

    :param id:
    :type id: str

    :rtype: Sample
    """

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


def samples_id_patch(id, new_sample=None):  # noqa: E501
    """samples_id_patch

    Update a sample. # noqa: E501

    :param id:
    :type id:
    :param new_sample: New properties for this sample
    :type new_sample: dict | bytes

    :rtype: Sample
    """

    old_sample = orm.Sample.query.get(id)
    if not old_sample:
        return Error(404, 'Not found'), 404

    if connexion.request.is_json:
        new_sample = Sample.from_dict(connexion.request.get_json())  # noqa: E501

    for prop in ['experiment_id', 'isolate_id']:
        if new_prop := getattr(new_sample, prop, None):
            setattr(old_sample, prop, new_prop)

    try:
        db.session.commit()
    except IntegrityError:
        return Error(409, 'Already existed'), 409
    else:
        return old_sample.to_model(), 200