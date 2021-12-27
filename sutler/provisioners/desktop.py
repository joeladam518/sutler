import click
import os
from ..application import Run
from git import Repo
from .provisioner import Provisioner
from ..installers import ComposerInstaller, DotfilesInstaller, FzfInstaller
from ..installers import NodeInstaller, PhpInstaller, SublimeInstaller


class DesktopProvisioner(Provisioner):
    def run(self):
        click.echo('Setting up your desktop environment')
        os.chdir(self.app.context.user.home)

        repos_path = os.path.join(self.app.context.user.home, 'repos')
        if not os.path.isdir(repos_path):
            os.mkdir(repos_path)

        ssh_path = os.path.join(self.app.context.user.home, '.ssh')
        if not os.path.isdir(ssh_path):
            os.mkdir(ssh_path)
            Run.command(f'cd "{ssh_path}" && ssh-keygen -t rsa')

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

        Run.command('update-alternatives --config editor', root=True)

        Repo.clone_from("https://github.com/magicmonty/bash-git-prompt.git", ".bash-git-prompt", depth=1)

        installer = DotfilesInstaller(self.ctx)
        installer.install('desktop')

        installer = FzfInstaller(self.ctx)
        installer.install()

        installer = PhpInstaller(self.ctx)
        installer.install('8.1', env='desktop')

        installer = ComposerInstaller(self.ctx)
        installer.install()

        installer = NodeInstaller(self.ctx)
        installer.install('16')

        installer = SublimeInstaller(self.ctx)
        installer.install('merge')

        # clone my public repos
        os.chdir(repos_path)
        Repo.clone_from('git@github.com:joeladam518/arduino-mqtt-led.git', 'arduino-mqtt-led')
        Repo.clone_from('git@github.com:joeladam518/BackupScripts.git', 'BackupScripts')
        Repo.clone_from('git@github.com:joeladam518/CurtainCallWP.git', 'CurtainCallWP')
        Repo.clone_from('git@github.com:joeladam518/colorschemes.git', 'colorschemes')
        Repo.clone_from('git@github.com:joeladam518/feather-mqtt-rgb-tree.git', 'feather-mqtt-rgb-tree')
        Repo.clone_from('git@github.com:joeladam518/feather-mqtt-temp-sensor.git', 'feather-mqtt-temp-sensor')
        Repo.clone_from('git@github.com:joeladam518/sutler.git', 'sutler')
