import click
import os
from ..application import Run
from .provisioner import Provisioner
from ..installers import DotfilesInstaller, FzfInstaller


class ServerProvisioner(Provisioner):
    def run(self) -> None:
        """
        Base configuration for a server
        :return: None
        """
        click.echo()
        click.echo('Setting up your server')
        click.echo()

        os.chdir(self.app.user.home)

        repos_path = os.path.join(self.app.user.home, 'repos')
        if not os.path.isdir(repos_path):
            os.mkdir(repos_path)

        ssh_path = os.path.join(self.app.user.home, '.ssh')
        if not os.path.isdir(ssh_path):
            os.mkdir(ssh_path)
            Run.command(f'cd "{ssh_path}" && ssh-keygen -t rsa')

        Run.update_and_upgrade()

        # Base stuff
        Run.install('apt-transport-https', 'build-essential', 'ca-certificates', 'software-properties-common')

        # Install utility applications
        Run.install('curl', 'git', 'htop', 'python3-pip', 'tmux', 'tree', 'vim')

        # Install the base stuff I like on all my servers
        DotfilesInstaller(self.ctx).install('server')
        FzfInstaller(self.ctx).install()
