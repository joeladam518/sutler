import click
import os


class User(object):
    def __init__(self, name: str, uid: int, gid: int):
        self.name = name
        self.home = os.path.expanduser(f"~{name}")
        self.uid = uid
        self.gid = gid

    def print(self):
        for key, value in vars(self).items():
            click.secho(f"{key}", nl=False, fg='bright_black')
            click.secho(f": {value}")
