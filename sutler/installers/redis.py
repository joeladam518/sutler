from ..support import Run
from .installer import Installer


class RedisInstaller(Installer):
    def install(self):
        Run.install('redis-server')

    def uninstall(self):
        Run.uninstall('redis-server')
