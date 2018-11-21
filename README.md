# Async Python Client for Kong

Forked from [aio-kong](https://github.com/lendingblock/aio-kong)
by [Luca Sbardella](https://github.com/lsbardel).

Changes to the original:
- Patch tests to work with >= Kong 0.14.x and 1.0.0rc2 works
  - TODO: Better backwards compatibility, support testing both 0.13 and >= 0.14.x
  - TODO: Pick the commit from history and PR it to original after this
- Add docker-compose [Kong stack](https://github.com/asyrjasalo/kongpose) for tests
  - TODO: Could be separate `make` rule or ignore if docker-compose is not installed
  - TODO: Add creating Kong Admin API loopback (either stack or cli `--option`)
- Add `Makefile` rules for flake8, mypy, testing, building and releasing
- Add separate `.venvs`  for dev and release, (re)created by Makefile rules
- Add some opinionated `pytest` plugins to help myself

## Requirements

- Python 3.6 or 3.7

## Installation

    pip install aio-kong-incubator

## CLI usage

The library installs ``kong`` commandline tool for updating Kong configuration:

    kong-incubator --yaml config.yaml

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

To start the test stack and run pytest:

    make test

Tests handle the cleanup of resources they have created.

See `Makefile` for all possible rules.
