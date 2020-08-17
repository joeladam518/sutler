import click
import os
import getpass
from .user import User


class Context(object):
    def __init__(self):
        self.paths = {}
        self.user = User(
            os.getuid(),
            os.getgid(),
            getpass.getuser(),
        )

    def get_path(self, key: str, default=None):
        return self.paths.get(key, default)

    def set_path(self, key: str, value):
        if not os.path.exists(value):
            raise FileNotFoundError('Path not found.')
        self.paths[key] = value

    def del_path(self, key: str):
        del self.paths[key]

    def print(self):
        click.secho("User", bold=True)
        for key, value in vars(self.user).items():
            click.secho(f"{key}", nl=False, fg='cyan')
            click.secho(f": {value}")

        click.echo()

        click.secho("Paths", bold=True)
        for key, value in self.paths.items():
            click.secho(f"{key}", nl=False, fg='cyan')
            click.secho(f": {value}")
