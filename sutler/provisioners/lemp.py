import click
import os
from ..installers import ComposerInstaller, MariadbInstaller, NginxInstaller
from ..installers import NodeInstaller, PhpInstaller
from .server import ServerProvisioner


class LempProvisioner(ServerProvisioner):
    def run(self) -> None:
        project = 'sutler-lemp'
        domain = 'ubuntu.sutler.test'
        php_version = '8.1'

        super().run()

        click.echo()
        click.echo('Setting up your lemp server')
        click.echo()

        os.chdir(self.app.user.home)

        installer = MariadbInstaller(self.ctx)
        installer.install()

        installer = NodeInstaller(self.ctx)
        installer.install('16')

        installer = PhpInstaller(self.ctx)
        installer.install(php_version, env='server')

        installer = ComposerInstaller(self.ctx)
        installer.install()

        installer = NginxInstaller(self.ctx)
        installer.install(project, domain, php_version)

        # TODO: Configure ufw
        # Run.command("ufw allow 'Nginx HTTP'", root=True)
        # Run.command("ufw allow 'Nginx HTTPS'", root=True)
        # click.echo()
        # click.echo('Checking ufw status:')
        # Run.command("ufw status", root=True)
        # click.echo()
