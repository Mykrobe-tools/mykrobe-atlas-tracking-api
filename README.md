# Development
## Prerequisites
* Docker
* Make sure the `pg_config` program is installed.
  * For example, on Ubuntu, install the `libpq-dev` package.
## Testing
Start the test database:
```
make testdb
```
Run tests:
```
make test
```

# Deployment

* The server inside the container listens on port `8080`.
* It accepts the `SQLALCHEMY_DATABASE_URI` environment variable.

For example:

```shell script
docker run -p <host_port>:8080 -e SQLALCHEMY_DATABASE_URI=<db_uri> <image_name>
```
