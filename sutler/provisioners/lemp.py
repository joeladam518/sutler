import click
import os
from .server import ServerProvisioner
from ..installers import ComposerInstaller, MariadbInstaller, NginxInstaller
from ..installers import NodeInstaller, PhpInstaller


class LempProvisioner(ServerProvisioner):
    def run(self):
        super().run()

        click.echo()
        click.echo('Setting up your lemp server')
        click.echo()

        os.chdir(self.app.context.user.home)

        installer = MariadbInstaller(self.ctx)
        installer.install()

        installer = NodeInstaller(self.ctx)
        installer.install('16')

        installer = PhpInstaller(self.ctx)
        installer.install('8.1', env='server')

        installer = ComposerInstaller(self.ctx)
        installer.install()

        installer = NginxInstaller(self.ctx)
        installer.install()
