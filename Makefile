install-dependencies:
	poetry install --no-root

run-local:
	poetry run python app

flake8-lint:
	poetry run flake8 .

build:
	docker build -t cofradia-api Dockerfile .

run:
	docker-compose up --build