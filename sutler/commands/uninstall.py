import click
from click.core import Context as ClickContext
from ..installers import FzfInstaller, NodeInstaller, PhpInstaller, RedisInstaller


@click.group()
def uninstall():
    pass


@click.command()
@click.pass_context
def fzf(ctx: ClickContext):
    installer = FzfInstaller(ctx)
    installer.uninstall()


@click.command()
@click.pass_context
def nodejs(ctx: ClickContext):
    installer = NodeInstaller(ctx)
    installer.uninstall()


@click.command()
@click.pass_context
@click.argument('version', type=str, required=True)
def php(ctx: ClickContext, version: str):
    installer = PhpInstaller(ctx)
    installer.uninstall(version)


@click.command()
@click.pass_context
def redis(ctx: ClickContext):
    installer = RedisInstaller(ctx)
    installer.uninstall()


uninstall.add_command(fzf)
uninstall.add_command(nodejs)
uninstall.add_command(php)
uninstall.add_command(redis)
