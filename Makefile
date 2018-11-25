.DEFAULT_GOAL := all

# At least OS X does not have this in default PATH, for `pip install --user`
PATH := ${HOME}/.local/bin:${PATH}

# virtualenv related
VENV_DEV_PATH := .venvs/dev
VENV_RELEASE_PATH := .venvs/release

# run tests for docker-compose env
KONG_ADMIN_URL := http://localhost:8001
KONG_ADMIN_KEY :=

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

_venv_dev:
	virtualenv --version >/dev/null || pip install --user virtualenv
	test -d "${VENV_DEV_PATH}" || virtualenv --no-site-packages "${VENV_DEV_PATH}"
	. "${VENV_DEV_PATH}/bin/activate" && \
	pip install --quiet -r requirements-dev.txt

_venv_release:
	virtualenv --version >/dev/null || pip install --user virtualenv
	virtualenv --no-site-packages --clear "${VENV_RELEASE_PATH}"
	. "${VENV_RELEASE_PATH}/bin/activate" && \
	pip install --upgrade pip setuptools wheel twine

flake8: ## Run flake8 for static code analysis
	. "${VENV_RELEASE_PATH}/bin/activate" && \
	flake8 kong/

mypy: ## Run mypy for static type checking
	. "${VENV_RELEASE_PATH}/bin/activate" && \
	mypy kong/

dc: ## Start docker-compose env on background
	git submodule update --init --recursive
	docker-compose --file testkong/docker-compose.yml up --detach

dc_rm: ## Stop and remove docker-compose env and volumes
	git submodule update --init --recursive
	docker-compose --file testkong/docker-compose.yml down --volumes

test: _venv_dev ## Run tests. Installs requirements first.
	. "${VENV_DEV_PATH}/bin/activate" && \
	pytest --cov --spec --instafail --diff-type=auto

retest: ## Run failed tests only. If none, run all.
	. "${VENV_DEV_PATH}/bin/activate" && \
	pytest --cov --spec --instafail --diff-type=auto \
		--last-failed --last-failed-no-failures all

build: _venv_release ## Build source dist and wheel
	. "${VENV_RELEASE_PATH}/bin/activate" && pip install --force-reinstall .
	##########################################
	### Sanity check before building dists ###
	. "${VENV_RELEASE_PATH}/bin/activate" && kong-incubator --version && \
	python setup.py clean --all bdist_wheel sdist

install: ## Install package from source tree
	pip install --force-reinstall .
	###############################################
	### Smoke check after installed from source ###
	kong-incubator --version

publish_testpypi: ## Publish dists to test.pypi.org
	. "${VENV_RELEASE_PATH}/bin/activate" && \
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	# pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple kong-incubator

publish_pypi: ## Publish dists to pypi.org
	. "${VENV_RELEASE_PATH}/bin/activate" && twine upload dist/*
	# pip installl --upgrade kong-incubator

all: test build install ## Run test, build and install

clean: ## Remove .venvs, builds, dists, and caches
	rm -rf dist build *.egg-info kong/__pycache__ tests/__pycache__
	rm -rf .venvs
	rm -rf .pytest_cache .mypy_cache
	rm -f .coverage
