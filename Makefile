generate:
	java -jar scripts/openapi-generator.jar generate -i swagger.yaml -g python-flask

build:
	docker build -t track .

run:
	docker run --rm -p 8080:8080 track

type_check:
	mypy openapi_server

test:
	pytest

clean:
	docker system prune -f --volumes
