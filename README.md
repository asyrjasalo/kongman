# Async Python Client for Kong (experimental fork of aio-kong)

Forked from [aio-kong](https://github.com/lendingblock/aio-kong)
by [Luca Sbardella](https://github.com/lsbardel).

Changes to the original:
  - Patch tests to pass with Kong 0.14.x and 1.0.0rc2
  - Added [docker-compose stack](https://github.com/asyrjasalo/kongpose) for tests
  - Added `Makefile` rules for linting, testing, building and publishing
  - Added separate `.venvs`  for dev and release, handled by `make` rules
  - Added (opinionated) `pytest` plugins for dev venv, to help myself
  - Added `KADMIN_` env vars for using via Kong Admin API loopback with key-auth

TODO:
  - Verify 0.14.x compatibility in production use
  - Tests for both 0.13 and >= 0.14.x (differences: SNIs, minor consumer diff)
  - PR Kong 0.14.x compatibility to original
  - Add an `--option` for creating Kong Admin API loopback service


## Installation

On Python >= 3.6:

    pip install --upgrade kong-incubator

## Usage

### CLI

Create or update the Kong resources according to configuration:

    kong-incubator --yaml config.yaml

By default, target `KONG_URL` is [http://localhost:8001](http://localhost:8001).

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
