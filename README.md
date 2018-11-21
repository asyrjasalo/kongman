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

- Python >= 3.6

## Installation

    pip install aio-kong-incubator

## CLI

Use `kong-incubator` commandline tool for updating Kong configuration:

    kong-incubator --yaml config.yaml

## From Python

```python
from kong.client import Kong

async with Kong() as cli:
    services = await cli.services.get_list()
    print(json.dumps(services, indent=4))
```

## Development

To start the `docker-compose` test stack and run tests with `pytest`:

    make test

Tests cleanup what they create so `docker volumes` are left intact,
unless `make testdown` is used.

Some other `make` rules (see `Makefile` for all):

- `make flake8`
- `make mypy`
- `make build`
- `make install` (install package user-wide)
- `make release_pypi`


