import click
from ..installers import PhpInstaller


@click.group()
def uninstall():
    pass


@click.command()
@click.argument('version', type=str, required=True)
def php(version):
    PhpInstaller.uninstall(version)


uninstall.add_command(php)
