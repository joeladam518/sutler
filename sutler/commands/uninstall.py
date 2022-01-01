import click
from click.core import Context as ClickContext
from ..installers import DotfilesInstaller, FzfInstaller, MariadbInstaller
from ..installers import NodeInstaller, PhpInstaller, RedisInstaller


@click.group()
def uninstall():
    pass


@click.command()
@click.pass_context
@click.argument('system', type=click.Choice(('desktop', 'mac', 'server')), required=True)
def dotfiles(ctx: ClickContext, system: str):
    installer = DotfilesInstaller(ctx)
    installer.uninstall(system)


@click.command()
@click.pass_context
def fzf(ctx: ClickContext):
    installer = FzfInstaller(ctx)
    installer.uninstall()


@click.command()
@click.pass_context
def mariadb(ctx: ClickContext):
    installer = MariadbInstaller(ctx)
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


uninstall.add_command(dotfiles)
uninstall.add_command(fzf)
uninstall.add_command(mariadb)
uninstall.add_command(nodejs)
uninstall.add_command(php)
uninstall.add_command(redis)
