import click
import os
from .user import User


class Context(object):
    def __init__(self, os_: str = None, user_: User = None):
        self.machine = None
        self.os = os_
        self.shell = os.environ['COMSPEC'] if os_ == 'windows' else os.environ['SHELL']
        self.paths = {}
        self.user = user_

    # Path Methods

    def get_path(self, key: str, default=None):
        return self.paths.get(key, default)

    def set_path(self, key: str, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError('Path not found.')
        self.paths[key] = path

    def del_path(self, key: str):
        del self.paths[key]

    # Debug functions

    def print(self):
        click.echo()
        click.secho("Operating System: ", fg='cyan')
        click.secho(f"{self.os}")
        click.echo()
        click.secho("User", fg='cyan')
        if self.user is not None:
            self.user.print()
        else:
            click.secho(f"{self.user}")
        click.echo()
        click.secho("Default shell", fg='cyan')
        click.secho(f"{self.shell}")
        click.echo()
        click.secho("Machine (The type of machine we're provisioning)", fg='cyan')
        click.secho(f"{self.machine}")
        click.echo()
        click.secho("Paths", fg='cyan')
        for key, value in self.paths.items():
            click.secho(f"{key}", nl=False, fg='bright_black')
            click.secho(f": {value}")
        click.echo()
