import os
import getpass
from jinja2 import Environment, FileSystemLoader
from .context import Context
from .singleton import SingletonMeta
from .user import User
from ..utils import get_os, is_root


class App(metaclass=SingletonMeta):
    def __init__(self):
        self.context = Context(get_os(), User(os.getuid(), os.getgid(), getpass.getuser()))
        self.context.set_path('root', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.context.set_path('templates', f"{self.context.get_path('root')}/templates")
        self.context.set_path('scripts', f"{self.context.get_path('root')}/scripts")
        self.jinja = Environment(loader=FileSystemLoader(self.context.get_path('templates')))

    def drop_privileges(self):
        if not is_root():
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

    def os_type(self):
        if self.context.os in ['debian', 'raspbian', 'ubuntu']:
            return 'debian'
        else:
            return self.context.os
