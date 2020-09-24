from uuid import UUID

from connexion.exceptions import BadRequestProblem


def validate_sample_id(id_: str):
    try:
        UUID(id_, version=4)
    except ValueError:
        raise BadRequestProblem