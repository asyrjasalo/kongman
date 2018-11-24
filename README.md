# kong-incubator (fork of aio-kong)

Declare the Kong you want in `yaml`, over using and documenting `curl` commands.

Partially incompat fork of [aio-kong](https://github.com/lendingblock/aio-kong)
by [Luca Sbardella](https://github.com/lsbardel). Changes:

  - Patched tests (SNI, consumer) to pass with Kong 0.14.x and 1.0.0rc2
  - Added [docker-compose stack](https://github.com/asyrjasalo/kongpose) for tests
  - Added `make` rules for `flake8`, `test`, `build`, `publish_pypi`, etc.
  - Added separate `.venvs`  for dev and release, handled by `make` rules
  - Added (opinionated) `pytest` plugins for dev venv, to help myself
  - Added `--output` to limit to a single property over whole JSON
  - Added `./examples` for Kong Admin API loopback and an example service via it
  - Added `KONG_ADMIN_KEY` for using Kong Admin API via the loopback and key-auth
  - Add`KONG_ADMIN_URL` that defaults to `http://localhost:8000`
  - Remove `KONG_URL` **BWIC**
  - Remove `--ip` **BWIC**

TODO:
  - Make compatible with Kong < 0.14, PR the Kong >= 0.14 changes to aio-kong


## Installation

On Python >= 3.6:

    pip install --upgrade kong-incubator

## Usage

`KONG_ADMIN_URL` defaults [http://localhost:8001](http://localhost:8001).

Create or upgrade resources (example [Mockbin](http://mockbin.org/) proxy):

    kong-incubator --yaml ./examples/mockbin.yaml

Generate a random `key` for the consumer:

    kong-incubator --key-auth mocker

Output only if key is already set.

See `kong-incubator --help` for all options.

### Securing Kong Admin API

This creates [Kong Admin API Loopback](https://docs.konghq.com/0.14.x/secure-admin-api/#kong-api-loopback).

Create the resources and get the `key` for admin:

    kong-incubator --yaml ./examples/kadmin.yaml
    kong-incubator --key-auth root --output key

Use Kong Admin API from now on:

    export KONG_ADMIN_KEY={{thekeyabove}}
    export KONG_ADMIN_URL=http://localhost:8000/kadmin
    kong-incubator --yaml ..

In Kubernetes/OpenShift, remove route to 8001 to prevent unauthorized access.

## .yaml

On upgrades, the created previous resources are not removed,
unless they expplicitly have `ensure: absent` defined in `yaml`.

### Usage as lib

```python
import json
from kong.client import Kong

async with Kong() as cli:
    services = await cli.services.get_list()
    print(json.dumps(services, indent=4))
```

## Development

Help yourself with `make` rules. If not helpful, please elaborate in issue.

Rules take care of [testkong/docker-compose.yml](https://github.com/asyrjasalo/kongpose/blob/master/docker-compose.yml) containing:
- Kong + PostgreSQL
- Konga (Admin webapp) + MongoDB

To create and start the env, run tests for it, build and install from source:

    make

Tests clean up the Kong resources they create. The Docker volumes for Kong's
PostgreSQL and Konga's MongoDB persist until `make dc_rm` or `make clean`.

Run `make clean` to reset everything, see `make help` for all options.
