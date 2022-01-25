import click
import os
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
            self.app.sys.exec(f'cd "{ssh_path}" && ssh-keygen -t rsa')

        self.app.sys.update_and_upgrade()

        # Base stuff
        self.app.sys.install('apt-transport-https', 'build-essential', 'ca-certificates', 'software-properties-common')

        # Install utility applications
        self.app.sys.install('curl', 'git', 'htop', 'python3-pip', 'tmux', 'tree', 'vim', 'virtualenv')

        # Install the base stuff I like on all my servers
        DotfilesInstaller(self.ctx).install('server')
        FzfInstaller(self.ctx).install()
