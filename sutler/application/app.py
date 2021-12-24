import os
import getpass
from .context import Context
from jinja2 import Environment, FileSystemLoader
from .singleton import SingletonMeta
from ..support import OS
from typing import Optional
from .user import User


class App(metaclass=SingletonMeta):
    """
    TODO: do I really need this singleton?
    """
    def __init__(self):
        self.context = Context(OS.type(), OS.type_like(), OS.shell(), User(getpass.getuser(), os.getuid(), os.getgid()))
        self.set_path('root', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.set_path('scripts', f"{self.get_path('root')}/scripts")
        self.set_path('templates', f"{self.get_path('root')}/templates")
        self.jinja = Environment(loader=FileSystemLoader(self.get_path('templates')))

    def del_path(self, key: str) -> None:
        del self.context.paths[key]

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

    def get_path(self, key: str) -> Optional[str]:
        return self.context.paths.get(key, None)

    def is_root(self) -> bool:
        return OS.is_root()

    def os_type(self) -> str:
        if self.context.os in ['debian', 'raspbian', 'ubuntu']:
            return 'debian'
        else:
            return self.context.os

    def set_path(self, key: str, path: str) -> None:
        if not os.path.exists(path):
            raise FileNotFoundError('Path not found.')
        self.context.paths[key] = path
