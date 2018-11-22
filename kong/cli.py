
import json
import asyncio

import click

import yaml as _yaml

from . import __version__
from .client import Kong, KongError
from .utils import local_ip


@click.command()
@click.option(
    '--version',
    is_flag=True,
    default=False,
    help='Display version and exit'
)
@click.option(
    '--ip',
    is_flag=True,
    default=False,
    help='Show local IP address'
)
@click.option(
    '--key-auth',
    help='Create or display an authentication key for a consumer'
)
@click.option(
    '--key-only',
    is_flag=True,
    default=False,
    help='Output only the key for the consumer, rather than the consumer'
)
@click.option(
    '--yaml', type=click.File('r'),
    help='Yaml configuration to upload'
)
@click.pass_context
def kong(ctx, version, ip, key_auth, key_only, yaml):
    if version:
        click.echo(__version__)
    elif ip:
        click.echo(local_ip())
    elif key_auth:
        return _run(_auth_key(ctx, key_auth, key_only))
    elif yaml:
        return _run(_yml(ctx, yaml))
    else:
        click.echo(ctx.get_help())


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


async def _yml(ctx, yaml):
    async with Kong() as cli:
        try:
            result = await cli.apply_json(_yaml.load(yaml))
            click.echo(json.dumps(result, indent=4))
        except KongError as exc:
            raise click.ClickException(str(exc))


async def _auth_key(ctx, consumer, key_only=False):
    async with Kong() as cli:
        try:
            c = await cli.consumers.get(consumer)
            keys = await c.key_auths()
            if keys:
                key = keys[0]
            else:
                key = await c.create_key_auth()
            if key_only:
                click.echo(key['key'])
            else:
                click.echo(json.dumps(key, indent=4))
        except KongError as exc:
            raise click.ClickException(str(exc))


def main():     # pragma    nocover
    kong()
