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

Create or update the Kong resources according to configuration:

    kong-incubator --yaml ./examples/mockbin.yaml

Create a key-auth for the consumer (if not already created) and output the `key`:

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

To create the `docker-compose` stack and run tests for it:

    make test

Tests clean up the Kong resources they create.
The docker volume for DB persists until `make testdown` or `make clean` is ran.

Run `make` for the list of rules.
