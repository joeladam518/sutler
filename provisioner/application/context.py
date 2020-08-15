import os
import getpass


class Context(object):
    def __init__(self):
        self.user = {
            'uid': os.getuid(),
            'name': getpass.getuser(),
            'home': os.path.expanduser("~")
        }
        self.paths = {}
        self.set_path('src', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.set_path('templates', f"{self.get_path('src')}/templates")

    def get_path(self, key: str, default=None):
        return self.paths.get(key, default)

    def set_path(self, key: str, value):
        if not os.path.exists(value):
            raise FileNotFoundError('Not found')
        self.paths[key] = value

    def del_path(self, key: str):
        del self.paths[key]

    def get_user(self, key: str, default=None):
        return self.user.get(key, default)

    def set_user(self, name, home, uid):
        self.user['name'] = name
        self.user['home'] = home
        self.user['uid'] = uid
