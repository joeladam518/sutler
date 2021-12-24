import click
from typing import Optional
from .user import User


class Context(object):
    def __init__(self, os_: str, os_like_: str, shell_: Optional[str], user_: User):
        self.os = os_
        self.os_like = os_like_
        self.shell = shell_
        self.user = user_

    def print(self):
        click.echo()
        click.secho("Operating System: ", fg='cyan')
        click.secho(f"{self.os}", fg='bright_white')
        click.echo()

        click.secho("Operating System like: ", fg='cyan')
        click.secho(f"{self.os_like}", fg='bright_white')
        click.echo()

        click.secho("Default shell", fg='cyan')
        click.secho(f"{self.shell}", fg='bright_white')
        click.echo()

        click.secho("User", fg='cyan')
        self.user.print()
        click.echo()
