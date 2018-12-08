import asyncio
import click
import json
import yaml as _yaml

from . import __version__
from .client import Kong, KongError


@click.command()
@click.option(
    "--admin-url",
    envvar="KONG_ADMIN_URL",
    help="Kong Admin API URL.\nDefault: http://localhost:8001\n"
    + "Precedence over KONG_ADMIN_URL",
)
@click.option(
    "--admin-key",
    envvar="KONG_ADMIN_KEY",
    help="Kong Admin API apikey if required.\nDefault: None\n"
    + "Precedence over KONG_ADMIN_KEY",
)
@click.option(
    "--key-auth", help="Consumer to generate a key or output the existing."
)
@click.option(
    "--yaml",
    type=click.File("r"),
    help="Defines one or many Kong resources by their target state.",
)
@click.option(
    "--output",
    default=True,
    help="If given, restrict output to this JSON property, or None.\n"
    + "By default, output everything.",
)
@click.option("--version", is_flag=True, help="Output version and exit.")
@click.pass_context
def kong(ctx, admin_url, admin_key, key_auth, yaml, output, version):
    if version:
        click.echo(__version__)
    elif key_auth:
        return _run(_auth_key(ctx, key_auth, output, admin_url, admin_key))
    elif yaml:
        return _run(_yml(ctx, yaml, output, admin_url, admin_key))
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


async def _yml(ctx, yaml, output, admin_url, admin_key):
    async with Kong(admin_url, admin_key=admin_key) as cli:
        try:
            result = await cli.apply_json(_yaml.load(yaml))
            if output:
                _output(result, output)
        except KongError as exc:
            raise click.ClickException(str(exc))


async def _auth_key(ctx, consumer, output, admin_url, admin_key):
    async with Kong(admin_url, admin_key=admin_key) as cli:
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


def main():  # pragma    nocover
    kong()
