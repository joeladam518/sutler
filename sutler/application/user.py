import click
import os


class User(object):
    def __init__(self, name: str, uid: int, gid: int, gids: tuple = ()):
        self.name = name
        self.home = os.path.expanduser(f"~{name}")
        self.uid = uid
        self.gid = gid
        self.gids = gids

    def print(self):
        for key, value in vars(self).items():
            click.secho(f"{key}", nl=False, fg='white')
            if key == 'gids':
                value = ', '.join(list(map(lambda gid: str(gid), value)))
            click.secho(f": {value}", fg='bright_white')
