from ..application import Run
from .installer import Installer


class ComposerInstaller(Installer):
    def install(self):
        Run.script(self.app.scripts_path('install-php-composer'))

    def uninstall(self):
        pass
