import click
from typing import Optional
from .user import User


class Context(object):
    def __init__(self, os_: str, os_like_: str, shell_: Optional[str], user_: User):
        self.os = os_
        self.os_like = os_like_
        self.paths = {}
        self.shell = shell_
        self.user = user_

    def print(self):
        click.echo()
        click.secho("Operating System: ", fg='cyan')
        click.echo(f"{self.os}")
        click.echo()

        click.secho("Operating System like: ", fg='cyan')
        click.echo(f"{self.os_like}")
        click.echo()

        click.secho("Default shell", fg='cyan')
        click.echo(f"{self.shell}")
        click.echo()

        click.secho("User", fg='cyan')
        if self.user is not None:
            self.user.print()
        else:
            click.echo(f"{self.user}")
        click.echo()

        click.secho("Paths", fg='cyan')
        for key, value in self.paths.items():
            click.secho(f"{key}", nl=False, fg='bright_black')
            click.secho(f": {value}")
        click.echo()
