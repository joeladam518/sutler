import click
from click.core import Context as ClickContext
from typing import Optional
from ..installers import ComposerInstaller, DotfilesInstaller, FzfInstaller, MariadbInstaller
from ..installers import NodeInstaller, PhpInstaller, RedisInstaller


@click.group()
def install():
    pass


@click.command()
@click.pass_context
@click.argument('system', type=click.Choice(('desktop', 'mac', 'server')), required=True)
def dotfiles(ctx: ClickContext, system: str):
    installer = DotfilesInstaller(ctx)
    installer.install(system)


@click.command()
@click.pass_context
def fzf(ctx: ClickContext):
    installer = FzfInstaller(ctx)
    installer.install()


@click.command()
@click.pass_context
@click.option('--db-name', 'db_name', type=str, default=None,
              help='The databases name.')
@click.option('--db-user', 'db_user', type=str, default=None,
              help='The database\'s user.')
def mariadb(ctx: ClickContext, db_name: Optional[str], db_user: Optional[str]):
    installer = MariadbInstaller(ctx)
    installer.install(db=db_name, user=db_user)


@click.command()
@click.pass_context
@click.argument('version', type=str, required=True)
def nodejs(ctx: ClickContext, version: str):
    installer = NodeInstaller(ctx)
    installer.install(version)


@click.command()
@click.pass_context
@click.argument('version', type=str, required=True)
@click.option('-e', '--env', 'environment', type=click.Choice(('desktop', 'dev', 'server')),
              default='desktop', help='The type of environment you\'re installing php on.')
@click.option('-a', '--add', 'add', type=str, multiple=True, default=(),
              help="Any additional extensions you might want to install.")
@click.option('-r', '--remove', 'remove', type=str, multiple=True, default=(),
              help="Extensions you want to exclude from installing.")
def php(ctx: ClickContext, version: str, environment: str, add: tuple, remove: tuple):
    installer = PhpInstaller(ctx)
    installer.install(version, environment, add, remove)


@click.command()
@click.pass_context
def php_composer(ctx: ClickContext):
    installer = ComposerInstaller(ctx)
    installer.install()


@click.command()
@click.pass_context
def redis(ctx: ClickContext):
    installer = RedisInstaller(ctx)
    installer.install()


install.add_command(dotfiles)
install.add_command(fzf)
install.add_command(mariadb)
install.add_command(nodejs)
install.add_command(php)
install.add_command(php_composer)
install.add_command(redis)
