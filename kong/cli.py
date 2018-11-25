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
    help='Consumer to generate a key or output the existing.'
)
@click.option(
    '--output',
    default=True,
    help='Limit output to specific JSON property, or e.g. None.'
)
@click.option(
    '--yaml', type=click.File('r'),
    help='Defines what Kong resources to create or upgrade.'
)
@click.pass_context
def kong(ctx, version, key_auth, output, yaml):
    if version:
        click.echo(__version__)
    elif key_auth:
        return _run(_auth_key(ctx, key_auth, output))
    elif yaml:
        return _run(_yml(ctx, yaml, output))
    else:
        click.echo(ctx.get_help())


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

def _output(response, query):
    if isinstance(query, bool):
        click.echo(json.dumps(response, indent=4))
    elif query in response:
        if isinstance(response[query], (str)):
            click.echo(response[query])
        else:
            click.echo(json.dumps(response[query], indent=4))

async def _yml(ctx, yaml, output):
    async with Kong() as cli:
        try:
            result = await cli.apply_json(_yaml.load(yaml))
            if output:
                _output(result, output)
        except KongError as exc:
            raise click.ClickException(str(exc))

async def _auth_key(ctx, consumer, output):
    async with Kong() as cli:
        try:
            c = await cli.consumers.get(consumer)
            keys = await c.key_auths()
            if keys:
                key = keys[0]
            else:
                key = await c.create_key_auth()
            if output:
                _output(key, output)
        except KongError as exc:
            raise click.ClickException(str(exc))


def main():     # pragma    nocover
    kong()
