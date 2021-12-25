import os
from .context import Context
from getpass import getuser
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
        user = User(getuser(), os.getuid(), os.getgid(), tuple(os.getgroups()))
        self.context = Context(OS.type(), OS.type_like(), OS.shell(), user)
        self.jinja = Environment(loader=FileSystemLoader(self.templates_path()))

    # TODO: This might not be needed. it seem if I only use sudo to escalate my subprocess calls then it's on the user
    #       to prove themselves and not my script. Keeping it around though
    def drop_privileges(self) -> None:
        if not OS.is_root():
            # We're not root so, like, whatever dude
            return

        # Reset the uid, guid, and groups back to the user who called this script
        os.setuid(self.context.user.uid)
        os.setgid(self.context.user.gid)
        os.setgroups(list(self.context.user.gids))

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
        return scripts_path if len(paths) == 0 else os.path.join(scripts_path, *paths)

    def templates_path(self, *paths: str) -> str:
        templates_path = os.path.join(self.base_path, 'templates')
        paths = list(map(lambda path: path.strip().rstrip(os.sep), paths))
        return templates_path if len(paths) == 0 else os.path.join(templates_path, *paths)
