import os
from .types import PosixSystem


class DebianSystem(PosixSystem):
    def install(self, *args: str) -> None:
        self.exec('apt install -y', *args, root=True)

    def uninstall(self, *args: str) -> None:
        # TODO: Which is the better way?
        # self.exec("apt-get purge -y", *args, root=True)
        # self.exec("apt-get --purge autoremove -y", root=True)
        self.exec('apt purge -y', *args, root=True)
        self.exec('apt autoremove -y', root=True)

    def update(self) -> None:
        self.exec('apt update', root=True)

    def update_and_upgrade(self) -> None:
        env = os.environ.copy()
        env['DEBIAN_FRONTEND'] = 'noninteractive'
        self.exec('apt update', root=True)
        self.exec('apt upgrade -y', root=True, env=env)
        self.exec('apt autoremove -y', root=True)
