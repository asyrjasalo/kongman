.DEFAULT_GOAL := all


# OS X does not have `pip install --user` target in default PATH
PATH := ${HOME}/.local/bin:${PATH}

# virtualenvs handled by rules below
VENV_DEV_PATH := .venvs/dev
VENV_RELEASE_PATH := .venvs/release

# lazily: package to download from PyPIs
PACKAGE_NAME = $(shell python setup.py --name)

# lazily: checks before building and after installing
SANITY_CHECK = kong-incubator --version
SMOKE_CHECK = kong-incubator --help


.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+[0-9]?*:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: _venv_dev
_venv_dev:
	virtualenv --version >/dev/null || pip install --user virtualenv
	test -d "${VENV_DEV_PATH}" || virtualenv --no-site-packages "${VENV_DEV_PATH}"
	. "${VENV_DEV_PATH}/bin/activate" && \
	pip install --quiet -r requirements-dev.txt

.PHONY: _venv_release
_venv_release:
	virtualenv --version >/dev/null || pip install --user virtualenv
	virtualenv --clear --no-site-packages "${VENV_RELEASE_PATH}"
	. "${VENV_RELEASE_PATH}/bin/activate" && \
	pip install --upgrade pip setuptools wheel

.PHONY: black
black: ## Reformat source code in-place
	. "${VENV_DEV_PATH}/bin/activate" && black .

.PHONY: flake8
flake8: ## Run flake8 for static code analysis
	. "${VENV_DEV_PATH}/bin/activate" && flake8

.PHONY: mypy
mypy: ## Run mypy for static type checking
	. "${VENV_DEV_PATH}/bin/activate" && mypy .

.PHONY: dc
dc: ## Start docker-compose env on background
	git submodule update --init --recursive
	docker-compose --file kongpose/docker-compose.yml up --detach

.PHONY: dc_rm
dc_rm: ## Stop and remove docker-compose env and volumes
	git submodule update --init --recursive
	docker-compose --file kongpose/docker-compose.yml down --volumes

.PHONY: test
test: _venv_dev ## Run tests (installs requirements first)
	. "${VENV_DEV_PATH}/bin/activate" && \
	pytest --cov --spec --instafail --diff-type=auto

.PHONY: retest
retest: ## Run failed tests only, if none, run all
	. "${VENV_DEV_PATH}/bin/activate" && \
	pytest --cov --spec --instafail --diff-type=auto \
		--last-failed --last-failed-no-failures all

.PHONY: build
build: _venv_release ## Build source dist and wheel
	. "${VENV_RELEASE_PATH}/bin/activate" && pip install .
	##########################################
	### Sanity check before building dists ###
	. "${VENV_RELEASE_PATH}/bin/activate" && ${SANITY_CHECK} && \
	python setup.py clean --all bdist_wheel sdist && \
	pip install --upgrade twine

.PHONY: install
install: ## Install package from source tree, as --editable
	pip install --editable .
	###############################################
	### Smoke check after installed from source ###
	${SMOKE_CHECK}

.PHONY: install_test
install_test: ## Install the latest test.pypi.org release
	pip install --force-reinstall \
		--index-url https://test.pypi.org/simple/ \
		--extra-index-url https://pypi.org/simple ${PACKAGE_NAME}

.PHONY: install_pypi
install_pypi: ## Install the latest PyPI release
	pip install --force-reinstall --upgrade ${PACKAGE_NAME}

.PHONY: uninstall
uninstall: ## Uninstall the package, regardless of its origin
	pip uninstall --yes ${PACKAGE_NAME}

.PHONY: publish_test
publish_test: ## Publish dists to test.pypi.org
	. "${VENV_RELEASE_PATH}/bin/activate" && \
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: publish_pypi
publish_pypi: ## Publish dists to PyPI
	. "${VENV_RELEASE_PATH}/bin/activate" && twine upload dist/*

.PHONY: all
all: test build install ## Run test, build and install

.PHONY: clean
clean: ## Remove .venvs, builds, dists, and caches
	rm -rf dist build *.egg-info **/__pycache__
	rm -rf .venvs
	rm -rf .pytest_cache .mypy_cache
	rm -f .coverage
