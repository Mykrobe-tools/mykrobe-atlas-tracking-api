import logging

from psycopg2.errorcodes import INVALID_TEXT_REPRESENTATION
from sqlalchemy.exc import DataError

logger = logging.getLogger(__name__)


def internal_server_error_handler(e):
    logger.error(e)
    if isinstance(e.original_exception, DataError):
        return sqlalchemy_data_error_handler(e.original_exception)


def sqlalchemy_data_error_handler(e):
    # TODO: In the future, when OpenAPI's server generator for Python can generate validator for this format, remove our manual one
    if e.orig and e.orig.pgcode == INVALID_TEXT_REPRESENTATION and 'uuid' in str(e.orig).lower():
        return 'Bad request', 400