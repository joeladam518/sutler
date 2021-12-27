import click
from click.core import Context as ClickContext
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
def lemp(ctx: ClickContext):
    provisioner = LempProvisioner(ctx)
    provisioner.run()


@click.command()
@click.pass_context
def server(ctx: ClickContext):
    provisioner = ServerProvisioner(ctx)
    provisioner.run()


setup.add_command(desktop)
setup.add_command(lemp)
setup.add_command(server)
