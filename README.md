# kongman (fork of aio-kong)

Declare the Kong you want in `yaml`, over manual `curl`s and keeping docs of them.
Uses Kong Admin API via async HTTP. Includes example to prevent unauthorized.

### Changelog

**BWIC** changes incompatible with [aio-kong](https://github.com/lendingblock/aio-kong)
by [Luca Sbardella](https://github.com/lsbardel).

  - Patch tests (SNI, consumer) to pass on Kong 0.14.x and 1.0.0rc2
  - Add [docker-compose stack](https://github.com/asyrjasalo/kongpose) for tests
  - Add `make` rules for `flake8`, `test`, `build`, `publish_pypi`, etc.
  - Add separate `.venvs` for dev and release, handled by `make` rules
  - Add (opinionated) `pytest` plugins, to help myself
  - Add `--output` to filter a single property out of whole JSON (for scripts)
  - Add `./examples` for Kong Admin API loopback and example endpoint via it
  - Add `KONG_ADMIN_KEY` to use Kong Admin API via loopback and key-auth
  - Add `KONG_ADMIN_URL`, defaults to `http://localhost:8000`
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

    kong-incubator --yaml ./examples/mockbin.yaml

Generate a random `key` for its consumer:

    kong-incubator --key-auth mocker

Output only if `key` is already set.

Re-running later `--yaml` file only upgrades the changed resources.
Removing resource(s) from file does not delete it from Kong,
unless the resource has `ensure: absent` defined in `.yaml`.

See `kong-incubator --help` for all options.

### Securing Kong Admin API

Creates [Kong Admin API Loopback](https://docs.konghq.com/0.14.x/secure-admin-api/#kong-api-loopback) to require key-auth :

    kong-incubator --yaml ./examples/kadmin.yaml
    kong-incubator --key-auth root --output key

Using Kong Admin API now requires `KONG_ADMIN_KEY`:

    export KONG_ADMIN_KEY={{thekeyabove}}
    export KONG_ADMIN_URL=http://localhost:8000/kadmin
    kong-incubator --yaml ..

In Kubernetes/OpenShift, remove the routes to 8001, 8444 to prevent unauthorized.

### Use as lib

```python
import json
from kong.client import Kong

async with Kong() as cli:
    services = await cli.services.get_list()
    print(json.dumps(services, indent=4))
```

## Development

Help yourself with `make` rules. If not helpful, please elaborate in an issue.

Rules use virtualenvs `.venvs/dev` testing and `./venvs/release` for building.

They also handle [testkong/docker-compose.yml](https://github.com/asyrjasalo/kongpose/blob/master/docker-compose.yml) containing:
- Kong + PostgreSQL
- Konga (Admin webapp) + MongoDB

To create the above, run tests on it, build the package and install it:

    make

Tests clean up the Kong resources they created. The Docker volumes for Kong's
PostgreSQL and Konga's MongoDB persist until `make dc_rm` or `make clean` is ran.
Running `make clean` remove also created `.venvs`, builds and any caches in repo.

See `make help` for all options.

### Publish

Release venv has `twine` to upload the created wheel and sdists over HTTPS.

Upload to [Test PyPI](https://test.pypi.org/project/kong-incubator):

    make publish_testpypi

Upload to [PyPI](https://pypi.org/project/kong-incubator)

    make publish_pypi
