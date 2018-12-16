# kongman (fork of aio-kong)

Declare the [Kong](https://konghq.com/kong-community-edition) you want,
with `yaml`. Stop manual `curl`s and maintaining docs of them.

Manages resources via Kong Admin API (REST,
[async HTTP](https://aiohttp.readthedocs.io/en/stable), JSON).
Includes [example](https://github.com/asyrjasalo/kongman/blob/master/examples/kadmin.yaml) to add authorization to the Admin API itself.

### Changelog

Some changes backwards incompatible with [aio-kong](https://github.com/lendingblock/aio-kong) by [Luca Sbardella](https://github.com/lsbardel).

- Patch tests (SNI, consumer) to pass on Kong 0.14.x and 1.0.0rc4
- Add [docker-compose stack](https://github.com/asyrjasalo/kongpose) for tests
- Add `make` rules `test`, `retest`, `build`, `install`, `publish_pypi`, ...
- Add creating `.venvs/` for dev and release, handled by `make` rules
- Add pytest plugins: `clarity`, `instafail` and `spec`, tests run in dev venv
- Add tools in dev venv: `pur` for reqs and `black`, `flake8`, `mypy` for code
- Add tools in release venv: `wheel` for bdist and `twine` for publish PyPis
- Add `--output` to limit output to a JSON property (for scripts), or have `None`
- Add `examples/` for Kong Admin API loopback and example endpoint via it
- Add `KONG_ADMIN_URL`, defaults to `http://localhost:8001`
- Add `KONG_ADMIN_KEY` to use Kong Admin API via loopback and key-auth
- Add `--admin-url` and `--admin-key` to take precedence over above two
- Remove `KONG_URL` **BWIC**
- Remove `--ip` **BWIC**

TODO:

- Add compatibility for <0.14 Kongs, PR the >=0.14 parts back to aio-kong


## Installation

From [PyPI](https://pypi.org/project/kong-incubator):

    pip install --upgrade kong-incubator

Python >= 3.6 required.


## Usage

`KONG_ADMIN_URL` defaults [http://localhost:8001](http://localhost:8001).

Create or upgrade [resources](https://github.com/asyrjasalo/kongman/blob/master/examples/mockbin.yaml) (is a proxy to [Mockbin](http://mockbin.org)):

    kong-incubator --yaml examples/mockbin.yaml

Generate a random `key` for its consumer:

    kong-incubator --key-auth mocker

Output consumer only if `key` has been already set.

Running with a changed `--yaml` only upgrades the changed parts.
Resources been removed from the file are not deleted from Kong.
To delete a resource from Kong, add `ensure: absent` for it in YAML.

For list of all options, run without any:

```
$ kong-incubator

Usage: kong-incubator [OPTIONS]

Options:
  --admin-url TEXT  Kong Admin API URL.
                    Default: http://localhost:8001
                    Precedence over KONG_ADMIN_URL
  --admin-key TEXT  Kong Admin API apikey if required.
                    Default: None
                    Precedence over KONG_ADMIN_KEY
  --key-auth TEXT   Consumer to generate a key or output the existing.
  --yaml FILENAME   Defines one or many Kong resources by their target
                    state.
  --output TEXT     If given, restrict output to this JSON property, or
                    None.
                    By default, output everything.
  --version         Output version and exit.
  --help            Show this message and exit.
```

### Securing Kong Admin API

Creates [Kong Admin API Loopback](https://docs.konghq.com/0.14.x/secure-admin-api/#kong-api-loopback) requiring key-auth:

    kong-incubator --yaml examples/kadmin.yaml
    kong-incubator --key-auth root --output key

From now on, manage Kong via the loopback (checks request header `apikey`):

    export KONG_ADMIN_URL=http://localhost:8000/kadmin
    export KONG_ADMIN_KEY={{thekeyabove}}
    kong-incubator --yaml ..

Options `--admin-url` or `--admin-key` can be used over, or to take precedence:

    export KONG_ADMIN_URL=http://localhost:8000/kadmin
    kong-incubator --admin-key={{thekeyabove}} --yaml ..

In Kubernetes/OpenShift, remove routes to 8001 and 8444.

### Use as lib

```python
import json
from kong.client import Kong

async with Kong() as cli:
    services = await cli.services.get_list()
    print(json.dumps(services, indent=4))
```


## Development

Tests assume you have Kong Admin API running at
[http://localhost:8001](http://localhost:8001).

If you have `docker-compose` available, you can run `make dc` to get
[kongpose/](https://github.com/asyrjasalo/kongpose/blob/master/docker-compose.yml)
as a git submodule and start it on background for tests.
Use `make dc_rm` to stop and remove the stack, including the volumes for DBs.

Run `make` as a shortcut for three other rules:

- `make test` creates `.venvs/dev` and installs requirements, also dev.
  To re-run only the failed tests if any, otherwise all, use
  `make retest` which skips installation of requirements(-dev).
  Both clean up the Kong resources they create.

- `make build` recreates `.venvs/release` on each run,
  installs build tools there and builds source and wheel dists ready to publish.

- `make install` installs the package from source tree.
  No need reinstalling after source edits as the package is installed editable.

You can `make --jobs` to run the above rules parallel, hence on 3 CPU cores.

Run `make pur` to [update requirements(-dev)](https://github.com/alanhamlett/pip-update-requirements) locked versions for the dependencies that have them.

Moreover, run `make {{tool}}` for
[black](https://black.readthedocs.io/en/stable/),
[flake8](http://flake8.pycqa.org/en/latest/) or
[mypy](http://mypy-lang.org/). Settings for `flake8` and `mypy`, as well as
[pytest](https://docs.pytest.org/en/latest/) are in their own config files
as they do not yet support `pyproject.toml`, like `black`.

Run `make clean` to remove `.venvs/`, `build/`, `dist/` and source tree caches.

See `make help` for all rules:

```
all                            Run test, build and install (default goal)
black                          Reformat source code in-place
build                          Build source dist and wheel
clean                          Remove .venvs, builds, dists, and caches
dc_rm                          Stop and remove docker-compose env and volumes
dc                             Start docker-compose env on background
flake8                         Run flake8 for static code analysis
install                        Install package from source tree, as --editable
install_pypi                   Install the latest PyPI release
install_test                   Install the latest test.pypi.org release
mypy                           Run mypy for static type checking
publish_pypi                   Publish dists to PyPI
publish_test                   Publish dists to test.pypi.org
pur                            Update requirements(-dev) for locked versions
retest                         Run failed tests only, if none, run all
test                           Run tests, installs requirements(-dev) first
uninstall                      Uninstall the package, regardless of its origin
```

### Publish

[Twine](https://twine.readthedocs.io/en/latest) included to upload over HTTPS.

To [Test PyPI](https://test.pypi.org/project/kong-incubator):

    make publish_test

To [PyPI](https://pypi.org/project/kong-incubator)

    make publish_pypi
