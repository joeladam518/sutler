import click
import os


class User(object):
    def __init__(self, uid: int, gid: int, name: str):
        self.uid = uid
        self.gid = gid
        self.name = name
        self.home = os.path.expanduser(f"~{name}")

    def print(self):
        for key, value in vars(self).items():
            click.secho(f"{key}", nl=False, fg='bright_black')
            click.secho(f": {value}")
