import click
import os
from getpass import getuser
from jinja2 import Environment, FileSystemLoader
from .context import Context
from .singleton import SingletonMeta
from ..support import OS
from .user import User


class App(metaclass=SingletonMeta):
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).rstrip(os.sep)
        self.context = Context()
        self.jinja = Environment(loader=FileSystemLoader(self.templates_path()))
        self.os = OS.type()
        self.os_like = OS.type_like()
        self.user = User(getuser(),  OS.shell(), os.getuid(), os.getgid(), tuple(os.getgroups()))

    def drop_privileges(self) -> None:
        """Drop any escalated privileges
        TODO: This function might not be needed. It seems like if I use subprocess and only escalate the
              user's privileges during those individual subprocess calls I won't escalate sutler's privileges...
              Maybe... Keeping it around just in case and until I'm sure I don't need it.

        :rtype: None
        """
        if not OS.is_root():
            # We're not root so, like, whatever dude
            return

        # Reset the uid, guid, and groups back to the user who called this script
        os.setuid(self.user.uid)
        os.setgid(self.user.gid)
        os.setgroups(list(self.user.gids))

        # Ensure a very conservative umask
        # 0o022 == 0755 for directories and 0644 for files
        # 0o027 == 0750 for directories and 0640 for files
        os.umask(0o027)

    def os_type(self) -> str:
        return 'debian' if self.os in ['debian', 'raspbian', 'ubuntu'] else self.os

    def path(self, *paths: str) -> str:
        paths = list(map(lambda path: path.strip().rstrip(os.sep), paths))
        return self.base_path if len(paths) == 0 else os.path.join(self.base_path, *paths)

    def print(self) -> None:
        click.echo()
        click.secho("Operating System", fg='cyan')
        click.secho(f"{self.os}", fg='bright_white')
        click.echo()

        click.secho("Operating System like", fg='cyan')
        click.secho(f"{self.os_like}", fg='bright_white')
        click.echo()

        click.secho("User", fg='cyan')
        self.user.print()
        click.echo()

        click.secho("Context", fg='cyan')
        self.context.print()
        click.echo()

        click.secho("Paths", fg='cyan')
        click.secho(f"base_path: ", nl=False, fg='bright_black')
        click.secho(f"{self.path()}", fg='bright_white')
        click.secho(f"scripts_path: ", nl=False, fg='bright_black')
        click.secho(f"{self.scripts_path()}", fg='bright_white')
        click.secho(f"templates_path: ", nl=False, fg='bright_black')
        click.secho(f"{self.templates_path()}", fg='bright_white')
        click.echo()

    def scripts_path(self, *paths: str) -> str:
        scripts_path = os.path.join(self.base_path, 'scripts')
        paths = list(map(lambda path: path.strip().rstrip(os.sep), paths))
        return scripts_path if len(paths) == 0 else os.path.join(scripts_path, *paths)

    def templates_path(self, *paths: str) -> str:
        templates_path = os.path.join(self.base_path, 'templates')
        paths = list(map(lambda path: path.strip().rstrip(os.sep), paths))
        return templates_path if len(paths) == 0 else os.path.join(templates_path, *paths)
