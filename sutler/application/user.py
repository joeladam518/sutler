import click
import os
from ..support import OS


class User:
    def __init__(self, name: str, shell: str, uid: int, gid: int, gids: tuple = ()):
        self.name = name
        self.home = os.path.expanduser(f"~{name}")
        self.shell = shell
        self.uid = uid
        self.gid = gid
        self.gids = gids

    def is_root(self) -> bool:
        return OS.is_root()

    def print(self) -> None:
        for key, value in vars(self).items():
            if isinstance(value, dict):
                value = ', '.join(['{}={}'.format(k, repr(v)) for k, v in value.items()])
            elif isinstance(value, (list, tuple)):
                value = ', '.join(list(map(lambda gid: str(gid), value)))
            click.secho(f"{key}: ", nl=False, fg='bright_black')
            click.secho(f"{value}", fg='bright_white')
