generate:
	java -jar scripts/openapi-generator.jar generate -i swagger.yaml -g python-flask

build:
	docker build -t dist .

type_check:
	mypy openapi_server

test:
	pytest

clean:
	docker system prune -f --volumes
