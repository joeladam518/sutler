import click
from ..support import Run


class RedisInstaller:
    @staticmethod
    def install():
        Run.command("apt install -y redis-server", root=True)
        output = Run.command("redis-cli ping", capture_output=True)

        if output == 'PONG':
            click.echo("Redis was installed successfully")

    @staticmethod
    def uninstall():
        Run.command("apt-get purge -y redis-server", root=True)
        Run.command("apt-get --purge autoremove -y", root=True)
