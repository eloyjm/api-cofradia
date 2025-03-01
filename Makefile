install-dependencies:
	poetry install --no-root

run-local:
	poetry run python app

flake8-lint:
	poetry run flake8 .