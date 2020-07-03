import connexion
import six

from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.event import Event  # noqa: E501
from openapi_server import util


def samples_id_events_event_id_delete(id, event_id):  # noqa: E501
    """samples_id_events_event_id_delete

    Delete an event with {eventId} associated with a sample with {id}. # noqa: E501

    :param id: 
    :type id: str
    :param event_id: 
    :type event_id: str

    :rtype: None
    """
    return 'do some magic!'


def samples_id_events_event_id_get(id, event_id):  # noqa: E501
    """samples_id_events_event_id_get

    Return an event with {eventId} associated with a sample with {id}. # noqa: E501

    :param id: 
    :type id: str
    :param event_id: 
    :type event_id: str

    :rtype: Event
    """
    return 'do some magic!'


def samples_id_events_get(id):  # noqa: E501
    """samples_id_events_get

    Return a list of events associated with a sample. # noqa: E501

    :param id: 
    :type id: str

    :rtype: List[Event]
    """
    return 'do some magic!'


def samples_id_events_post(id, event):  # noqa: E501
    """samples_id_events_post

    Add a new event to be associated with a sample. # noqa: E501

    :param id: 
    :type id: str
    :param event: Event to be added
    :type event: dict | bytes

    :rtype: Event
    """
    if connexion.request.is_json:
        event = Event.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
