from openapi_server import orm
from openapi_server.models.error import Error  # noqa: E501


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
