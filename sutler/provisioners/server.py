import click
import os
from ..application import Run
from .provisioner import Provisioner
from ..installers import DotfilesInstaller, FzfInstaller


class ServerProvisioner(Provisioner):
    def run(self):
        click.echo('Setting up your server')
        os.chdir(self.app.context.user.home)

        if not os.path.isdir('./repos'):
            os.mkdir('repos')

        Run.update_and_upgrade()

        # Base stuff
        Run.install('apt-transport-https', 'ca-certificates', 'software-properties-common')

        # Install utility applications
        Run.install('curl', 'git', 'htop', 'python3-pip', 'tmux', 'tree', 'vim')

        installer = DotfilesInstaller(self.ctx)
        installer.install('server')

        installer = FzfInstaller(self.ctx)
        installer.install()
