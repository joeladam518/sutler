import click
from ..installers import PhpInstaller


@click.command()
@click.argument('version', type=str, required=True)
def php(version):
    PhpInstaller.uninstall(version)


@click.group()
def uninstall():
    pass


uninstall.add_command(php)
