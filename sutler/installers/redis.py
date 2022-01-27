from .installer import Installer


class RedisInstaller(Installer):
    def install(self) -> None:
        self.app.os.update()
        self.app.os.install('redis-server')

    def uninstall(self) -> None:
        self.app.os.uninstall('redis-server')
