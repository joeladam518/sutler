import click
from .installer import Installer


class NginxInstaller(Installer):
    def install(self) -> None:
        self.app.os.exec.update()
        self.app.os.exec.install('nginx')

    def uninstall(self) -> None:
        self.app.os.exec.uninstall('nginx')
