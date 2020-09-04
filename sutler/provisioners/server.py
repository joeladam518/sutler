import click
from .provisioner import Provisioner


class ServerProvisioner(Provisioner):
    def run(self):
        click.echo('Setting up your generic server')
