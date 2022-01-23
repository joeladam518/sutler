import click
import os
from git import Repo
from ..installers import ComposerInstaller, DotfilesInstaller, FzfInstaller
from ..installers import NodeInstaller, PhpInstaller, SublimeInstaller
from .provisioner import Provisioner


class DesktopProvisioner(Provisioner):
    def run(self) -> None:
        """
        Provision my ubuntu desktop machine

        NOTE: This script will probably have to be updated before it is run every single time...

        Color for terminal screen (to mimic iTerm):
        -------------------------------------------
        black dark   = #000000   black light    = #686868
        red dark     = #c91b00   red light      = #ff6e67
        green dark   = #00c200   green light    = #5ffa68
        yellow dark  = #C7B700   yellow light   = #fffc67
        blue dark    = #0532e1   blue light     = #5075ff #42A5F5
        magenta dark = #ca30c7   magenta light  = #ff77ff
        cyan dark    = #00c5c7   cyan light     = #60fdff
        white dark   = #D7D7D7   white light    = #ffffff

        :return: None
        """
        click.echo()
        click.echo('Setting up your desktop environment')
        click.echo()

        os.chdir(self.app.user.home)

        repos_path = os.path.join(self.app.user.home, 'repos')
        if not os.path.isdir(repos_path):
            os.mkdir(repos_path)

        ssh_path = os.path.join(self.app.user.home, '.ssh')
        if not os.path.isdir(ssh_path):
            os.mkdir(ssh_path)
            self.app.system.exec(f'cd "{ssh_path}" && ssh-keygen -t rsa')

        self.app.system.update_and_upgrade()

        # Base stuff
        self.app.system.install('apt-transport-https', 'build-essential', 'ca-certificates', 'software-properties-common')

        # Install restricted extras
        if self.app.system.type == 'ubuntu':
            self.app.system.install('ubuntu-restricted-extras', 'ubuntu-restricted-addons')

        # Install some useful applications
        self.app.system.install('curl', 'git', 'gnome-tweak-tool', 'htop', 'mosquitto-clients', 'mariadb-client',
                         'python3-pip', 'ripit', 'tmux', 'tree', 'vim-gtk3', 'virtualenv')

        # Install bash git prompt
        os.chdir(self.app.user.home)
        Repo.clone_from("https://github.com/magicmonty/bash-git-prompt.git", ".bash-git-prompt", depth=1)

        # Install the ability to work with exfat drives
        self.app.system.install('exfat-utils', 'exfat-fuse')

        # Install some snaps
        self.app.system.exec('snap refresh')
        self.app.system.exec('snap install audacity gimp vlc')

        # Install even more stuff
        DotfilesInstaller(self.ctx).install('desktop')
        FzfInstaller(self.ctx).install()
        PhpInstaller(self.ctx).install('8.1', env='desktop')
        ComposerInstaller(self.ctx).install()
        NodeInstaller(self.ctx).install('16')
        SublimeInstaller(self.ctx).install('merge')

        # Update the command line editor to vim (Has to be done manually)
        self.app.system.exec('update-alternatives --config editor', root=True)

        # Clone my public repos
        if click.confirm('Install repos?'):
            os.chdir(repos_path)
            Repo.clone_from('git@github.com:joeladam518/arduino-mqtt-led.git', 'arduino-mqtt-led')
            Repo.clone_from('git@github.com:joeladam518/BackupScripts.git', 'BackupScripts')
            Repo.clone_from('git@github.com:joeladam518/CurtainCallWP.git', 'CurtainCallWP')
            Repo.clone_from('git@github.com:joeladam518/colorschemes.git', 'colorschemes')
            Repo.clone_from('git@github.com:joeladam518/feather-mqtt-rgb-tree.git', 'feather-mqtt-rgb-tree')
            Repo.clone_from('git@github.com:joeladam518/feather-mqtt-temp-sensor.git', 'feather-mqtt-temp-sensor')
            Repo.clone_from('git@github.com:joeladam518/sutler.git', 'sutler')

        click.echo()
        click.echo("Reminder of the other programs you like, but unfortunately their installation can't be automated")
        click.echo("yet...")
        click.echo()
        click.echo("* Arduino - https://www.arduino.cc/en/software")
        click.echo("* Chrome - https://www.google.com/chrome/")
        click.echo("* dbeaver - https://dbeaver.io/")
        click.echo("* Jetbrains IDE - https://www.jetbrains.com/toolbox-app/")
        click.echo("* Postman - https://www.postman.com/downloads/?utm_source=postman-home")
        click.echo("* Slack - https://slack.com/downloads/linux")
        click.echo("* Vagrant - https://www.vagrantup.com/downloads")
        click.echo("* Virtual-Box - https://www.virtualbox.org/wiki/Linux_Downloads")
        click.echo("* Visual Studio Code - https://code.visualstudio.com/docs/setup/linux")
        click.echo()
