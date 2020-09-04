import click
from .provisioner import Provisioner


class DesktopProvisioner(Provisioner):
    def run(self):
        click.echo('Setting up your desktop environment');
