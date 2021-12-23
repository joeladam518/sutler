import click
import os
from git import Repo
from ..application import App
from ..support import run
from .provisioner import Provisioner


class ServerProvisioner(Provisioner):
    def run(self):
        click.echo('Setting up your generic server')

        os.chdir(self.app.context.user.home)

        if not os.path.isdir('./repos'):
            os.mkdir('repos')

        if not os.path.isdir('./repos/dotfiles'):
            Repo.clone_from('https://github.com/joeladam518/dotfiles.git', './repos/dotfiles')

        if not os.path.isdir('./repos/dotfiles'):
            self.ctx.fail('dotfiles was no cloned.')

        Run

        click.secho('Your server is now provisioned.')
