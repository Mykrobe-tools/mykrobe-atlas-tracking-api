#!/usr/bin/env python3

import connexion

from openapi_server import encoder
from openapi_server.db import init_db, migrate


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    init_db(app.app)
    app.add_api('openapi.yaml', arguments={'title': 'Tracking API'})
    migrate()

    app.run(port=8080)


if __name__ == '__main__':
    main()
