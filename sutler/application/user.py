import os


class User(object):
    def __init__(self, uid: int, gid: int, name: str):
        self.uid = uid
        self.gid = gid
        self.name = name
        self.home = os.path.expanduser(f"~{name}")
