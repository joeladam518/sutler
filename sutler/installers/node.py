import click
import os
from ..support import Run
from .installer import Installer

node_versions = (
    '14',
    '15',
    '16',
    '17'
)


class NodeInstaller(Installer):
    def install(self, version: str) -> None:
        if version not in node_versions:
            self.ctx.fail('Invalid node version')
        Run.command(f"curl -sL \"https://deb.nodesource.com/setup_{version}.x\" | sudo -E bash -")
        Run.install('nodejs')

    def uninstall(self) -> None:
        Run.uninstall('nodejs')
        # TODO: Do I have to remove the apt gpg key?
        if os.path.exists('/etc/apt/sources.list.d/nodesource.list'):
            Run.command('rm /etc/apt/sources.list.d/nodesource.list', root=True)
        Run.command('apt update', root=True)
