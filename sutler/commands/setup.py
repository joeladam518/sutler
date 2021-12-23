import click
from ..provisioners import DesktopProvisioner, LempProvisioner, ServerProvisioner


@click.command()
@click.pass_context
def desktop(ctx):
    provisioner = DesktopProvisioner(ctx)
    provisioner.run()


@click.command()
@click.pass_context
def lemp(ctx):
    provisioner = LempProvisioner(ctx)
    provisioner.run()


@click.command()
@click.pass_context
def server(ctx):
    provisioner = ServerProvisioner(ctx)
    provisioner.run()


@click.group()
def setup():
    pass


setup.add_command(desktop)
setup.add_command(lemp)
setup.add_command(server)
