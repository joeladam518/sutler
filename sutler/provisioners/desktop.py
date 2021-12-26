import click
import os
from ..application import Run
from git import Repo
from .provisioner import Provisioner
from ..installers import ComposerInstaller, DotfilesInstaller, FzfInstaller
from ..installers import MariadbInstaller, NodeInstaller, PhpInstaller


class DesktopProvisioner(Provisioner):
    def run(self):
        click.echo('Setting up your desktop environment')
        os.chdir(self.app.context.user.home)

        if not os.path.isdir('./repos'):
            os.mkdir('./repos')

        if not os.path.isdir('./.themes'):
            os.mkdir('./.themes')

        if not os.path.isdir('./.icons'):
            os.mkdir('./.icons')

        Run.update_and_upgrade()

        # Base stuff
        Run.install('apt-transport-https', 'software-properties-common', 'build-essential')

        # Install utility applications
        Run.install('curl', 'git', 'htop', 'mysql-client', 'python3-pip', 'tmux', 'tree', 'vim', 'xsel')

        if self.app.context.os == 'ubuntu':
            # Installing restricted extras
            Run.install('ubuntu-restricted-extras', 'ubuntu-restricted-addons')

        # Install the ability to work with exfat drives
        Run.install('exfat-utils', 'exfat-fuse')

        Run.command('snap refresh')
        Run.command('snap install vlc spotify gimp')

        installer = DotfilesInstaller(self.ctx)
        installer.install('desktop')

        Repo.clone_from("https://github.com/magicmonty/bash-git-prompt.git", ".bash-git-prompt", depth=1)

        installer = FzfInstaller(self.ctx)
        installer.install()

        installer = PhpInstaller(self.ctx)
        installer.install('8.1', env='desktop')

        installer = ComposerInstaller(self.ctx)
        installer.install()

        installer = NodeInstaller(self.ctx)
        installer.install('16')
