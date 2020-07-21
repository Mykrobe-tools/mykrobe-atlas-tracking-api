#!/usr/bin/env python3
import os

import connexion

from openapi_server import encoder
from openapi_server.db import db


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder

    app.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    db.init_app(app.app)
    db.app = app.app

    app.add_api('openapi.yaml', arguments={'title': 'Tracking API'})
    db.create_all()

    app.run(port=8080)


if __name__ == '__main__':
    main()
