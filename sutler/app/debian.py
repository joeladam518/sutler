import os
from .posix import PosixSystem
from .os import Sys


class DebianSystem(PosixSystem):
    @property
    def codename(self):
        """Return the codename for the debian system"""
        return Sys.release_info('VERSION_CODENAME')

    def install(self, *args: str) -> None:
        """Install a program"""
        self.exec('apt install -y', *args, root=True)

    def uninstall(self, *args: str) -> None:
        """Uninstall a program"""
        # TODO: Which is the better way?
        # self.exec("apt-get purge -y", *args, root=True)
        # self.exec("apt-get --purge autoremove -y", root=True)
        self.exec('apt purge -y', *args, root=True)
        self.exec('apt autoremove -y', root=True)

    def update(self) -> None:
        """Update the package repository"""
        self.exec('apt update', root=True)

    def update_and_upgrade(self) -> None:
        """Update the package repository and upgrade the systems packages"""
        env = os.environ.copy()
        env['DEBIAN_FRONTEND'] = 'noninteractive'
        self.exec('apt update', root=True)
        self.exec('apt upgrade -y', root=True, env=env)
        self.exec('apt autoremove -y', root=True)
