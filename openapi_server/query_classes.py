from flask_sqlalchemy import BaseQuery

from openapi_server.validators import validate_sample_id


class SampleQueryClass(BaseQuery):
    def get(self, ident):
        validate_sample_id(ident)
        return super().get(ident)