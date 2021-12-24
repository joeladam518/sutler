from ..application import Run
from .installer import Installer


class ComposerInstaller(Installer):
    def install(self):
        scripts_path = self.app.get_path('scripts')
        Run.script(f"{scripts_path}/install-php-composer")

    def uninstall(self):
        pass
