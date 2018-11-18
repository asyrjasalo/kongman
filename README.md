# Async Python Client for Kong

Forked from [aio-kong](https://github.com/lendingblock/aio-kong)
by [Luca Sbardella](https://github.com/lsbardel),

Changes to the original:
- Tests upgraded to work with >= Kong 0.14.x (was 0.13)
  - Intent to contribute back to original, as soon as have verified in prod
  - Target to support both 0.13 and >= 0.14.x
  - Maybe test with 1.0.0rc as well
- Tidy up `.venvs`, add `Makefile` for building and testing
  - Opinionated, for myself
- Add some useful `pytest` plugins
  - Opinionated, for myself

## Requirements

- Python >=3.6

## Installation

    pip install aio-kong-014

## CLI usage

The library installs ``kong`` commandline tool for updating Kong configuration:

    kong --yaml config.yaml

## Lib usage

The Python client can be imported with:

```python
from kong.client import Kong
```

Then used in async code:

```python
async with Kong() as cli:
    services = await cli.services.get_list()
    print(json.dumps(services, indent=4))
```

### Development

An [empty Kong API Gateway](https://github.com/asyrjasalo/kongpose)
must be started before running tests.

To run tests using pytest:

    make test

Tests handle the cleanup of resources they have created.
