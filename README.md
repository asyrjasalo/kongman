# Async Python Client for Kong (exp fork of aio-kong)

Forked from [aio-kong](https://github.com/lendingblock/aio-kong)
by [Luca Sbardella](https://github.com/lsbardel).

For managing Kong using declarative configuration (`yaml`),
over manual bookeeping of `curl`s and/or resource state handling `bash` scripts.

Changes to the original:
  - Patch tests to pass with Kong 0.14.x and 1.0.0rc2
  - Added [docker-compose stack](https://github.com/asyrjasalo/kongpose) for tests
  - Added `make` rules for `flake8`, `test`, `build`, `publish_pypi`, etc.
  - Added separate `.venvs`  for dev and release, handled by `make` rules
  - Added (opinionated) `pytest` plugins for dev venv, to help myself
  - Added `--key-only` to output only the consumer key, instead of whole JSON
  - Added `./examples` for Kong Admin API loopback and an example service via it
  - Added `KADMIN_APIKEY` for using Kong Admin API via the loopback and key-auth

TODO:
  - PR Kong 0.14.x to original if can make it compatible with 0.13
  - Maybe add `--init-loopback` for creating the  Kong Admin API loopback service


## Installation

On Python >= 3.6:

    pip install --upgrade kong-incubator

## Usage

### CLI

By default, target `KONG_URL` is [http://127.0.0.1:8001](http://127.0.0.1:8001).

Create or update the Kong resources from to configuration:

    kong-incubator --yaml ./examples/mockbin.yaml

Create a consumer key-auth `key`, if none exists, and output it:

    kong-incubator --key-auth mocker --key-only

Run `kong-incubator` for the list of options.

### Python

```python
from kong.client import Kong

async with Kong() as cli:
    services = await cli.services.get_list()
    print(json.dumps(services, indent=4))
```

## Development

For `docker-compose` env, running tests, building and installing from source:

    make

Tests clean up the Kong resources they create, docker volumes for Kong's
PostgreSQL and Konga's MongoDB persist until `make dc_down` or `make clean`.

Run `make clean` to reset everything, run `make help` for other options.
