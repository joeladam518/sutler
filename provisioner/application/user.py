import os


class User(object):
    def __init__(self, uid: int, name: str):
        self.uid = uid
        self.name = name
        self.home = os.path.expanduser(f"~{name}")
