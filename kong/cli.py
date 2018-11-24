import asyncio
import click
import json
import yaml as _yaml

from . import __version__
from .client import Kong, KongError


@click.command()
@click.option(
    '--version',
    is_flag=True,
    help='Output version and exit.'
)
@click.option(
    '--key-auth',
    help='Consumer to generate a key to, or output existing.'
)
@click.option(
    '--output',
    help='Output only this property over whole JSON.'
)
@click.option(
    '--yaml', type=click.File('r'),
    help='Declaration of Kong resources to create or upgrade.'
)
@click.pass_context
def kong(ctx, version, key_auth, output, yaml):
    if version:
        click.echo(__version__)
    elif key_auth:
        return _run(_auth_key(ctx, key_auth, output))
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


async def _auth_key(ctx, consumer, output=None):
    async with Kong() as cli:
        try:
            c = await cli.consumers.get(consumer)
            keys = await c.key_auths()
            if keys:
                key = keys[0]
            else:
                key = await c.create_key_auth()
            if output:
                click.echo(key[output])
            else:
                click.echo(json.dumps(key, indent=4))
        except KongError as exc:
            raise click.ClickException(str(exc))


def main():     # pragma    nocover
    kong()
