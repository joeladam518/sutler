from .installer import Installer


class RedisInstaller(Installer):
    def install(self) -> None:
        self.app.sys.update()
        self.app.sys.install('redis-server')

    def uninstall(self) -> None:
        self.app.sys.uninstall('redis-server')
