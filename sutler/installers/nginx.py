from .installer import Installer


class NginxInstaller(Installer):
    def install(self) -> None:
        self.app.os.update()
        self.app.os.install('nginx')

    def uninstall(self) -> None:
        self.app.os.uninstall('nginx')
