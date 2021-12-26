from ..application import Run
from .installer import Installer


class RedisInstaller(Installer):
    def install(self) -> None:
        Run.update()
        Run.install('redis-server')

    def uninstall(self) -> None:
        Run.uninstall('redis-server')
