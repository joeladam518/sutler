import os
from .installer import Installer


class NodeInstaller(Installer):
    versions = ('14', '15', '16', '17')

    def install(self, version: str) -> None:
        if version not in self.versions:
            self.ctx.fail('Invalid node version')
        self.app.os.exec(f"curl -sL \"https://deb.nodesource.com/setup_{version}.x\" | sudo -E bash -")
        self.app.os.install('nodejs')

    def uninstall(self) -> None:
        self.app.os.uninstall('nodejs')
        # TODO: Do I have to remove the apt gpg key?
        if os.path.exists('/etc/apt/sources.list.d/nodesource.list'):
            self.app.os.exec('rm /etc/apt/sources.list.d/nodesource.list', root=True)
        self.app.os.exec('apt update', root=True)
