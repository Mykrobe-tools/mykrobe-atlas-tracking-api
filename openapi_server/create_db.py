from openapi_server.factories.db import db


def main():
    db.create_all()


if __name__ == '__main__':
    main()