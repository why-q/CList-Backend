from pathlib import Path

import click
from alembic import config
from click import Context

from app import __version__
from app.api.server import Server
from app.config import settings
from app.utils.utils import chdir


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("-V", "--version", is_flag=True, help="Show version and exit.")
def main(ctx: Context, version):
    if version:
        click.echo(__version__)
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.option(
    "-h", "--host", show_default=True, help=f"Host IP. Default: {settings.SERVER.HOST}"
)
@click.option(
    "-p", "--port", show_default=True, help=f"Port. Default: {settings.SERVER.PORT}"
)
@click.option("--level", help="Log Level")
def server(host, port, level):
    kwargs = {
        "LOG.LEVEL": level,
        "SERVER.HOST": host,
        "SERVER.PORT": port,
    }
    for name, value in kwargs.items():
        if value:
            settings.set(name, value)

    Server().run()


@main.command()
@click.pass_context
@click.option('-h', '--help', is_flag=True)
@click.argument('args', nargs=-1)
def migrate(ctx: Context, help, args):
    with chdir(Path(__file__).parent / 'migration'):
        argv = list(args)
        if help:
            argv.append('--help')
        config.main(prog=ctx.command_path, argv=argv)
        
