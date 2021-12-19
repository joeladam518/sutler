import click
from ..support import Run


class RedisInstaller:
    @staticmethod
    def install():
        Run.command("apt install -y redis-server", root=True)
        output = Run.command("redis-cli ping", capture_output=True)

        if output == 'PONG':
            click.echo("Redis was installed successfully")
