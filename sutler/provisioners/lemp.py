import click
from .server import ServerProvisioner


class LempProvisioner(ServerProvisioner):
    def run(self):
        super().run()
        click.echo('Setting up your lemp server')
