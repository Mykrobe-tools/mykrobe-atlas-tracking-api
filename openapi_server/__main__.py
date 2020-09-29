#!/usr/bin/env python3

from openapi_server.factories.app import create_app


def main():
    app = create_app()
    app.run(port=8080)


if __name__ == '__main__':
    main()
