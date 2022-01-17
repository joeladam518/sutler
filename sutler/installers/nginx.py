import click
from ..application import Run
from .installer import Installer


class NginxInstaller(Installer):
    def install(self) -> None:
        Run.update()
        Run.install('nginx')

    def uninstall(self) -> None:
        Run.uninstall('nginx')
