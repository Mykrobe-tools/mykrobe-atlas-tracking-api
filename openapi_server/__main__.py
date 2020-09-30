#!/usr/bin/env python3
from openapi_server.app import app


def main():
    app.run(port=8080)


if __name__ == '__main__':
    main()
