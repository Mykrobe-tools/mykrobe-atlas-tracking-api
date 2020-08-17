generate:
	java -jar scripts/openapi-generator.jar generate -i swagger.yaml -g python-flask

build:
	docker build -t track .

run:
	docker run --rm -p 8080:8080 track

type_check:
	mypy openapi_server

testdb:
	docker run --rm -it -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust postgres

test:
	pytest

clean:
	docker system prune -f --volumes
