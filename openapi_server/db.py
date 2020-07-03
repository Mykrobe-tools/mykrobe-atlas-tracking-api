from flask import g
from flask_sqlalchemy import SQLAlchemy


def get_db():
    if 'db' not in g:
        g.db = SQLAlchemy()

    return g.db


def init_db(app):
    db = get_db()
    db.init_app(app)


def migrate():
    db = get_db()
    db.create_all()
