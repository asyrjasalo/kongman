.DEFAULT_GOAL := help

# Some environments (OS X) do not have this in PATH for `pip install --user`
PATH := ${HOME}/.local/bin:${PATH}

# virtualenv related
VENV_DEV_PATH := .venvs/dev
VENV_RELEASE_PATH := .venvs/release

help:
	@echo "Usage: make TARGET [ANOTHER_TARGET]..."

_venv_dev:
	virtualenv --version >/dev/null || pip install --user virtualenv
	test -d "${VENV_DEV_PATH}" || virtualenv "${VENV_DEV_PATH}"
	. "${VENV_DEV_PATH}/bin/activate"
	pip install --upgrade pip
	pip install --quiet -r requirements-dev.txt

_venv_release:
	virtualenv --version >/dev/null || pip install --user virtualenv
	virtualenv --clear "${VENV_RELEASE_PATH}"
	. "${VENV_RELEASE_PATH}/bin/activate"
	pip install --upgrade pip setuptools wheel twine

flake8: _venv_dev
	flake8 kong/

mypy: _venv_dev
	mypy kong/

install:
	pip install --user --force-reinstall .
	### smoke check after user-wide install ###
	kong-incubator

build: _venv_release
	### sanity check before building ###
	pip install .
	python setup.py clean --all bdist_wheel sdist

publish_testpypi: _venv_release
	twine upload --repository-url https://test.pypi.org/legacy/ --skip-existing dist/*

publish_pypi: _venv_release
	twine upload dist/*

test: _venv_dev
	docker-compose --file testkong/docker-compose.yml up --detach \
		kong-database kong-migration kong
	KADMIN_SECRET="k0n64dm1n" pytest --cov --spec --instafail --diff-type=auto

testdown:
	docker-compose --file testkong/docker-compose.yml down --volumes

all: test build

clean: testdown
	rm -rf dist build *.egg-info kong/__pycache__
	rm -rf .venvs
	rm -rf .pytest_cache .mypy_cache
	rm -f .coverage
