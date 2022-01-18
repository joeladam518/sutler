import click
from click.core import Context as ClickContext
from typing import Optional
from ..provisioners import DesktopProvisioner, LempProvisioner, ServerProvisioner


@click.group()
def setup():
    pass


@click.command()
@click.pass_context
def desktop(ctx: ClickContext):
    provisioner = DesktopProvisioner(ctx)
    provisioner.run()


@click.command()
@click.pass_context
@click.argument('domain', type=str, required=True)
@click.option('--php-version', type=click.Choice(('8.1', '8.0', '7.4')), default='8.1',
              help='The php version you would like to install')
@click.option('--project', type=str, default=None,
              help="The project name you would like to use. (For folders and such)")
def lemp(ctx: ClickContext, domain: str, php_version: str, project: Optional[str]):
    provisioner = LempProvisioner(ctx)
    provisioner.run(domain, php_version, project)


@click.command()
@click.pass_context
def server(ctx: ClickContext):
    provisioner = ServerProvisioner(ctx)
    provisioner.run()


setup.add_command(desktop)
setup.add_command(lemp)
setup.add_command(server)
