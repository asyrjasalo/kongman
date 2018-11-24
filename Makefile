.DEFAULT_GOAL := all

# Some environments (OS X) do not have this in PATH for `pip install --user`
PATH := ${HOME}/.local/bin:${PATH}

# virtualenv related
VENV_DEV_PATH := .venvs/dev
VENV_RELEASE_PATH := .venvs/release

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

_venv_dev:
	virtualenv --version >/dev/null || pip install --user virtualenv
	test -d "${VENV_DEV_PATH}" || virtualenv "${VENV_DEV_PATH}"
	. "${VENV_DEV_PATH}/bin/activate"
	pip install --quiet -r requirements-dev.txt

_venv_release:
	virtualenv --version >/dev/null || pip install --user virtualenv
	virtualenv --clear "${VENV_RELEASE_PATH}"
	. "${VENV_RELEASE_PATH}/bin/activate"
	pip install --upgrade pip setuptools wheel twine

flake8: _venv_dev ## Run flake8 for static code analysis
	flake8 kong/

mypy: _venv_dev ## Run mypy for static type checking
	mypy kong/

dc_get: ## Upgrade to the latest docker-compose env
	git submodule update --init --recursive

dc_up: ## Start docker-compose env on background
	docker-compose --file testkong/docker-compose.yml up --detach

dc_rm: ## Stop and remove docker-compose env and volumes
	docker-compose --file testkong/docker-compose.yml down --volumes

test: _venv_dev ## Run tests for KONG_ADMIN_URL, cleanup after
	pytest --cov --spec --instafail --diff-type=auto

retest: ## Re-run only the failed tests
	pytest --cov --spec --instafail --diff-type=auto \
		--last-failed --last-failed-no-failures none

build: _venv_release ## Build Python dists ready for `publish_`
	python setup.py clean --all bdist_wheel sdist

install: ## Pip (re)install user-wide from local git HEAD.
	pip install --user --force-reinstall .
	###################################
	### smoke checking the CLI next ###
	kong-incubator

publish_testpypi: _venv_release ## Publish the `build` dists to test.pypi.org
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish_pypi: _venv_release ## Publish the `build` dists to pypi.org
	twine upload dist/*

all: dc_get dc_up test build install ## Start testenv, test, build and install

clean: dc_get dc_rm ## Purge testenv, .venvs, dists, and tool caches
	rm -rf dist build *.egg-info kong/__pycache__ tests/__pycache__
	rm -rf .venvs
	rm -rf .pytest_cache .mypy_cache
	rm -f .coverage
