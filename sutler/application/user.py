import click
import os
from typing import Optional


class User:
    def __init__(self, name: str, shell: str, **kwargs):
        self.name: str = name
        self.shell: str = shell
        self.home: str = os.path.expanduser(f"~{name}")
        self.uid: Optional[int] = kwargs.get('uid', None)
        self.gid: Optional[int] = kwargs.get('gid', None)
        self.gids: Optional[tuple] = kwargs.get('gids', None)

    def print(self) -> None:
        for key, value in vars(self).items():
            if isinstance(value, dict):
                value = ', '.join(['{}={}'.format(k, repr(v)) for k, v in value.items()])
            elif isinstance(value, (list, tuple)):
                value = ', '.join(list(map(lambda gid: str(gid), value)))
            click.secho(f"{key}: ", nl=False, fg='bright_black')
            click.secho(f"{value}", fg='bright_white')
