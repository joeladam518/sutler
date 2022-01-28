import os
from .installer import Installer


class NodeInstaller(Installer):
    versions = ('14', '15', '16', '17')
    __source_file_path = '/etc/apt/sources.list.d/nodesource.list'

    def install(self, version: str) -> None:
        if version not in self.versions:
            self.ctx.fail('Invalid node version')
        os.chdir(self.app.user.home)
        self.app.os.exec(f"curl -sL \"https://deb.nodesource.com/setup_{version}.x\" | sudo -E bash -")
        self.app.os.install('nodejs')

    def uninstall(self) -> None:
        os.chdir(self.app.user.home)
        self.app.os.uninstall('nodejs')
        # TODO: Do I have to remove the apt gpg key?
        if os.path.exists(self.__source_file_path):
            self.app.os.rm(self.__source_file_path, root=True)
        self.app.os.update()
