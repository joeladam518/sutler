import os
import getpass


class App(object):
    def __init__(self):
        self.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.os_types = ('debian', 'ubuntu', 'raspberry pi os')
        self.machine_types = ('desktop', 'server', 'lamp', 'lemp', 'mqtt')
        self.user_uid = None
        self.user_name = None
        self.user_home = None

    def set_user(self):
        self.user_uid = os.getuid()
        self.user_name = getpass.getuser()
        self.user_home = os.path.expanduser("~")


if __name__ != '__main__':
    app = App()
