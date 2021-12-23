from ..support import Run


class RedisInstaller:
    @staticmethod
    def install():
        Run.install('redis-server')

    @staticmethod
    def uninstall():
        Run.uninstall('redis-server')
