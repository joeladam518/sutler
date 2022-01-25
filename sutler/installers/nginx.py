from .installer import Installer


class NginxInstaller(Installer):
    def install(self) -> None:
        self.app.sys.update()
        self.app.sys.install('nginx')

    def uninstall(self) -> None:
        self.app.sys.uninstall('nginx')
