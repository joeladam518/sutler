import click
from ..installers import PhpInstaller, NodeInstaller


@click.group()
def install():
    pass


@install.command()
def dotfiles():
    click.echo("Installing dotfiles!")


@install.command()
def fzf():
    click.echo("Installing fzf!")


@install.command()
def mariadb():
    click.echo("Installing mariadb!")


@install.command()
@click.argument('version', type=str, required=True)
def nodejs(version):
    NodeInstaller.install(version)


@install.command()
@click.argument('version', type=str, required=True)
@click.option('-e', '--env', 'environment', type=str, default='desktop',
              help='The environment on witch to install php on.')
@click.option('-a', '--additional', 'additional', type=str, multiple=True, default=(),
              help="Any additional extension you might want to install")
@click.option('-x', '--exclude', 'exclude', type=str, multiple=True, default=(),
              help="Extension you want to exclude from installing")
def php(version, environment, additional, exclude):
    PhpInstaller.install(version, environment, additional, exclude)


@install.command()
def php_composer():
    click.echo("Installing composer!")


@install.command()
def redis():
    click.echo("Installing redis!")


install.add_command(dotfiles)
install.add_command(fzf)
install.add_command(mariadb)
install.add_command(nodejs)
install.add_command(php)
install.add_command(php_composer)
install.add_command(redis)
