gendiff:
	poetry run gendiff

build:
	poetry build

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 gendiff

test-coverage:
	poetry run pytest --cov gendiff/

test:
	poetry run pytest