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
	pip install --upgrade pip setuptools wheel

test: _venv_dev
	pytest --spec --instafail --diff-type=auto

build: _venv_release
	pip install .
	python setup.py clean --all bdist_wheel sdist
	pip install --upgrade twine

publish_testpypi: _venv_release
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish_pypi: _venv_release
	twine upload dist/*

all: test build

clean:
	rm -rf dist build kong/*.egg-info kong/__pycache__
	rm -rf "${VENV_DEV_PATH}" "${VENV_RELEASE_PATH}"
	rm -rf .pytest_cache
