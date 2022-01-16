import click
import os
from ..support import OS
from typing import Optional


class User:
    def __init__(self, name: str, shell: str, uid: Optional[int] = None, gid: Optional[int] = None, gids: tuple = ()):
        self.name: str = name
        self.home: str = os.path.expanduser(f"~{name}")
        self.shell: str = shell
        self.uid: int = uid
        self.gid: int = gid
        self.gids: tuple = gids

    def print(self) -> None:
        for key, value in vars(self).items():
            if isinstance(value, dict):
                value = ', '.join(['{}={}'.format(k, repr(v)) for k, v in value.items()])
            elif isinstance(value, (list, tuple)):
                value = ', '.join(list(map(lambda gid: str(gid), value)))
            click.secho(f"{key}: ", nl=False, fg='bright_black')
            click.secho(f"{value}", fg='bright_white')
