import os
from .installer import Installer


class NodeInstaller(Installer):
    versions = ('14', '15', '16', '17')

    def install(self, version: str) -> None:
        if version not in self.versions:
            self.ctx.fail('Invalid node version')
        self.app.system.exec(f"curl -sL \"https://deb.nodesource.com/setup_{version}.x\" | sudo -E bash -")
        self.app.system.install('nodejs')

    def uninstall(self) -> None:
        self.app.system.uninstall('nodejs')
        # TODO: Do I have to remove the apt gpg key?
        if os.path.exists('/etc/apt/sources.list.d/nodesource.list'):
            self.app.system.exec('rm /etc/apt/sources.list.d/nodesource.list', root=True)
        self.app.system.exec('apt update', root=True)
