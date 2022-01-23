import click
import os
from getpass import getuser
from jinja2 import Environment, FileSystemLoader
from .context import Context
from ..operating_systems import DebianSystem
from .singleton import SingletonMeta
from ..support import OS
from .user import User


class App(metaclass=SingletonMeta):
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).rstrip(os.sep)
        self.context = Context()
        self.jinja = Environment(loader=FileSystemLoader(self.templates_path()))
        self.user = User(getuser(), OS.shell())

        if self.os.type != 'windows':
            self.user.uid = os.getuid()
            self.user.gid = os.getgid()
            self.user.gids = tuple(os.getgroups())
        # TODO: When we start operating systems that are not debian based we will need to
        #       refactor this to a factory that figures that out and instantiates the right os class
        self.system = DebianSystem(app=self, type=OS.type(), type_like=OS.type_like())

    def is_root(self) -> bool:
        return OS.is_root()

    def path(self, *paths: str) -> str:
        paths = list(map(lambda path: path.strip().rstrip(os.sep), paths))
        return self.base_path if len(paths) == 0 else os.path.join(self.base_path, *paths)

    def print(self) -> None:
        click.echo()
        click.secho("Operating System", fg='cyan')
        click.secho(f"{self.system.type}", fg='bright_white')
        click.echo()

        click.secho("Operating System like", fg='cyan')
        click.secho(f"{self.system.type_like}", fg='bright_white')
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

    def sys_path(self, *paths) -> str:
        paths = list(map(lambda path: path.strip().rstrip(os.sep), paths))
        return OS.root_path() if len(paths) == 0 else os.path.join(OS.root_path(), *paths)

    def templates_path(self, *paths: str) -> str:
        templates_path = os.path.join(self.base_path, 'templates')
        paths = list(map(lambda path: path.strip().rstrip(os.sep), paths))
        return templates_path if len(paths) == 0 else os.path.join(templates_path, *paths)
