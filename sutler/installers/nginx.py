from .installer import Installer


class NginxInstaller(Installer):
    def install(self) -> None:
        self.app.system.update()
        self.app.system.install('nginx')

    def uninstall(self) -> None:
        self.app.system.uninstall('nginx')
