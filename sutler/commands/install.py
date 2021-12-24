import click
from click.core import Context as ClickContext
from ..installers import ComposerInstaller, DotfilesInstaller, FzfInstaller, MariadbInstaller
from ..installers import NodeInstaller, PhpInstaller, RedisInstaller


@click.group()
def install():
    pass


@click.command()
@click.pass_context
def composer(ctx: ClickContext):
    installer = ComposerInstaller(ctx)
    installer.install()


@click.command()
@click.pass_context
def dotfiles(ctx: ClickContext):
    installer = DotfilesInstaller(ctx)
    installer.install()


@click.command()
@click.pass_context
def fzf(ctx: ClickContext):
    installer = FzfInstaller(ctx)
    installer.install()


@click.command()
@click.pass_context
def mariadb(ctx: ClickContext):
    installer = MariadbInstaller(ctx)
    installer.install()


@click.command()
@click.pass_context
@click.argument('version', type=str, required=True)
def nodejs(ctx: ClickContext, version: str):
    installer = NodeInstaller(ctx)
    installer.install(version)


@click.command()
@click.pass_context
@click.argument('version', type=str, required=True)
@click.option('-e', '--env', 'environment', type=str, default='desktop',
              help='The environment on witch to install php on.')
@click.option('-a', '--additional', 'additional', type=str, multiple=True, default=(),
              help="Any additional extension you might want to install")
@click.option('-x', '--exclude', 'exclude', type=str, multiple=True, default=(),
              help="Extension you want to exclude from installing")
def php(ctx: ClickContext, version: str, environment: str, additional: tuple, exclude: tuple):
    installer = PhpInstaller(ctx)
    installer.install(version, environment, additional, exclude)


@click.command()
@click.pass_context
def php_composer(ctx: ClickContext):
    installer = PhpInstaller(ctx)
    installer.install_composer()


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
