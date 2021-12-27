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
        Run.install('apt-transport-https', 'software-properties-common', 'build-essential')

        # Install utility applications
        Run.install('curl', 'git', 'htop', 'mysql-client', 'python3-pip', 'tmux', 'tree', 'vim', 'xsel')

        installer = DotfilesInstaller(self.ctx)
        installer.install('desktop')

        installer = FzfInstaller(self.ctx)
        installer.install()
