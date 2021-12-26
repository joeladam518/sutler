import click
from .server import ServerProvisioner
from ..installers import ComposerInstaller, MariadbInstaller, NodeInstaller, PhpInstaller


class LempProvisioner(ServerProvisioner):
    def run(self):
        super().run()
        click.echo('Setting up your lemp server')

        installer = PhpInstaller(self.ctx)
        installer.install('8.1', env='desktop')

        installer = ComposerInstaller(self.ctx)
        installer.install()

        installer = NodeInstaller(self.ctx)
        installer.install('16')

        installer = MariadbInstaller(self.ctx)
        installer.install()
