from ..application import Run
from .installer import Installer


class RedisInstaller(Installer):
    def install(self):
        Run.update()
        Run.install('redis-server')

    def uninstall(self):
        Run.uninstall('redis-server')
