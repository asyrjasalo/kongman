# kongman (fork of aio-kong)

Declare the [Kong](https://konghq.com/solutions/gateway/) you want, with `yaml`.
Stop manual `curl`s and maintaining docs of them.
Manages resources via Kong Admin API (REST, async HTTP, JSON).
Includes an example to add authorization to the Admin API itself.

### Changelog

Some changes backwards incompatible with [aio-kong](https://github.com/lendingblock/aio-kong) by [Luca Sbardella](https://github.com/lsbardel).

  - Patch tests (SNI, consumer) to pass on Kong 0.14.x and 1.0.0rc2
  - Add [docker-compose stack](https://github.com/asyrjasalo/kongpose) for tests
  - Add `make` rules for `flake8`, `mypy`, `test`, `build`, `publish_pypi`, ...
  - Add creating `.venvs/` for dev and release, handled by `make` rules
  - Add (opinionated) `pytest` plugins, to help myself
  - Add `--output` to limit output to a JSON property (for scripts), or have `None`
  - Add `examples/` for Kong Admin API loopback and example endpoint via it
  - Add `KONG_ADMIN_URL`, defaults to `http://localhost:8001`
  - Add `KONG_ADMIN_KEY` to use Kong Admin API via loopback and key-auth
  - Add `--admin-url` and `--admin-key` to take precedence over above two
  - Remove `KONG_URL` **BWIC**
  - Remove `--ip` **BWIC**

TODO:
  - Add compatibility for <0.14 Kongs, PR the >=0.14 parts back to aio-kong.


## Installation

From [PyPI](https://pypi.org/project/kong-incubator):

    pip install --upgrade kong-incubator

Python >= 3.6 required.

## Usage

`KONG_ADMIN_URL` defaults [http://localhost:8001](http://localhost:8001).

Create or upgrade resources (is a [Mockbin](http://mockbin.org) proxy):

    kong-incubator --yaml examples/mockbin.yaml

Generate a random `key` for its consumer:

    kong-incubator --key-auth mocker

Output only if `key` has been already set.

Running with a changed `--yaml` only upgrades the changed parts.
Resources been removed from the file are not deleted from Kong.
To delete a resource from Kong, add `ensure: absent` for it in YAML.

See `kong-incubator --help` for all options.

### Securing Kong Admin API

Creates [Kong Admin API Loopback](https://docs.konghq.com/0.14.x/secure-admin-api/#kong-api-loopback) requiring key-auth:

    kong-incubator --yaml examples/kadmin.yaml
    kong-incubator --key-auth root --output key

From now on, manage Kong via the loopback (checks request header `apikey`):

    export KONG_ADMIN_URL=http://localhost:8000/kadmin
    export KONG_ADMIN_KEY={{thekeyabove}}
    kong-incubator --yaml ..

Options `--admin-url` or `--admin-key` can be used instead, or to take precedence:

    export KONG_ADMIN_URL=http://localhost:8000/kadmin
    kong-incubator --admin-key={{thekeyabove}} --yaml ..

In Kubernetes/OpenShift, remove routes to 8001 and 8444 .

### Use as lib

```python
import json
from kong.client import Kong

async with Kong() as cli:
    services = await cli.services.get_list()
    print(json.dumps(services, indent=4))
```

## Development

Tests assume you have Kong Admin API running at [http://localhost:8001](http://localhost:8001).

If you have `docker-compose` available, you can run `make dc` to get
[kongpose/](https://github.com/asyrjasalo/kongpose/blob/master/docker-compose.yml) as a git submodule and start it on background for tests.
Use `make dc_rm` to stop and remove the stack, including the volumes for DBs.

Run `make` as a shortcut for three other rules:

- `make test` creates `.venvs/dev` that has also dev requirements installed.
To re-run only the failed tests, if any, use `make retest` which also skips
installation of requirements. Both clean up the Kong resources they create.

- `make build` creates `.venvs/release` on each run,
installs build tools and builds source and wheel dists.

- `make install` to install package from source tree.

Run `make clean` to remove `.venvs`, builds, dists and caches.

See `make help` for all options.

### Publish

[Twine](https://twine.readthedocs.io/en/latest) included for uploading over HTTPS.

To [Test PyPI](https://test.pypi.org/project/kong-incubator):

    make publish_test

To [PyPI](https://pypi.org/project/kong-incubator)

    make publish_pypi
