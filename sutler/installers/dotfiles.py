import os
from .installer import Installer


class DotfilesInstaller(Installer):
    def install(self):
        home_dir = self.app.context.user.home
        os.chdir(home_dir)

    def uninstall(self):
        home_dir = self.app.context.user.home
        os.chdir(home_dir)
