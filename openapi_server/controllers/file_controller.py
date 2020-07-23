import connexion
import six

from openapi_server.models.error import Error  # noqa: E501
from openapi_server import util, orm


def files_md5sum_get(md5sum):  # noqa: E501
    """files_md5sum_get

    Return a file based on a file md5sum. # noqa: E501

    :param md5sum:
    :type md5sum: str

    :rtype: File
    """

    resource = orm.File.query.get(md5sum)
    if not resource:
        return Error(404, 'Not found'), 404

    return resource.to_model(), 200


def samples_id_files_get(id):  # noqa: E501
    """samples_id_files_get

    Return a list of files associated with a sample. # noqa: E501

    :param id:
    :type id: str

    :rtype: List[File]
    """
    return 'do some magic!'


def samples_id_files_md5sum_delete(id, md5sum):  # noqa: E501
    """samples_id_files_md5sum_delete

    Delete a file with {md5sum} associated with a sample with {id}. # noqa: E501

    :param id:
    :type id: str
    :param md5sum:
    :type md5sum: str

    :rtype: None
    """
    return 'do some magic!'


def samples_id_files_md5sum_get(id, md5sum):  # noqa: E501
    """samples_id_files_md5sum_get

    Return a file with {md5sum} associated with a sample with {id}. # noqa: E501

    :param id:
    :type id: str
    :param md5sum:
    :type md5sum: str

    :rtype: File
    """
    return 'do some magic!'


def samples_id_files_post(id, file):  # noqa: E501
    """samples_id_files_post

    Add a new file to be associated with a sample. # noqa: E501

    :param id:
    :type id: str
    :param file: File to be added
    :type file: dict | bytes

    :rtype: File
    """
    if connexion.request.is_json:
        file = File.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
