import os
import getpass
from .context import Context
from jinja2 import Environment, FileSystemLoader
from .singleton import SingletonMeta
from ..support import OS
from .user import User


class App(metaclass=SingletonMeta):
    """
    TODO: do I really need this singleton?
    """
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).rstrip(os.sep)
        self.context = Context(OS.type(), OS.type_like(), OS.shell(), User(getpass.getuser(), os.getuid(), os.getgid()))
        self.jinja = Environment(loader=FileSystemLoader(self.templates_path()))

    def drop_privileges(self) -> None:
        if not OS.is_root():
            # We're not root so, like, whatever dude
            return

        # Remove group privileges
        os.setgroups([])

        # Try setting the new uid/gid
        os.setuid(self.context.user.uid)
        os.setgid(self.context.user.gid)

        # Ensure a very conservative umask
        # 0o022 == 0755 for directories and 0644 for files
        # 0o027 == 0750 for directories and 0640 for files
        os.umask(0o027)

    def path(self, *paths: str) -> str:
        paths = list(map(lambda path: path.strip().rstrip(os.sep), paths))
        return self.base_path if len(paths) == 0 else os.path.join(self.base_path, *paths)

    def is_root(self) -> bool:
        return OS.is_root()

    def os_type(self) -> str:
        return 'debian' if self.context.os in ['debian', 'raspbian', 'ubuntu'] else self.context.os

    def scripts_path(self, *paths: str) -> str:
        scripts_path = os.path.join(self.base_path, 'scripts')
        paths = list(map(lambda path: path.strip().rstrip(os.sep), paths))
        return scripts_path if len(paths) == 0 else os.path.join(self.base_path, *paths)

    def templates_path(self, *paths: str):
        templates_path = os.path.join(self.base_path, 'templates')
        paths = list(map(lambda path: path.strip().rstrip(os.sep), paths))
        return templates_path if len(paths) == 0 else os.path.join(self.base_path, *paths)
