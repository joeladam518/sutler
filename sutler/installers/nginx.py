import click
from .installer import Installer


class NginxInstaller(Installer):
    def install(self) -> None:
        self.app.system.exec.update()
        self.app.system.exec.install('nginx')

    def uninstall(self) -> None:
        self.app.system.exec.uninstall('nginx')
