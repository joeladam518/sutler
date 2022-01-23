from .installer import Installer


class RedisInstaller(Installer):
    def install(self) -> None:
        self.app.system.update()
        self.app.system.install('redis-server')

    def uninstall(self) -> None:
        self.app.system.uninstall('redis-server')
