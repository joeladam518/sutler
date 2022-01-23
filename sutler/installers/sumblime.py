from ..helpers import installed
from .installer import Installer


class SublimeInstaller(Installer):
    __source = 'deb https://download.sublimetext.com/ apt/stable/'
    __source_file_path = '/etc/apt/sources.list.d/sublime-text.list'

    def install(self, program: str) -> None:
        if program not in ('text', 'merge'):
            self.ctx.fail("Error: Invalid program name. Valid values are {text|merge}.")

        self.app.system.exec('wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -')
        self.app.system.exec(f'echo "{self.__source}" | sudo tee {self.__source_file_path}', root=True)
        self.app.system.update()
        self.app.system.install(f'sublime-{program}')

    def uninstall(self, program: str) -> None:
        if program not in ('text', 'merge'):
            self.ctx.fail("Error: Invalid program name. Valid values are {text|merge}.")

        self.app.system.uninstall(f'sublime-{program}')

        if not installed('sublime-text') and not installed('sublime-merge'):
            self.app.system.exec(f'rm {self.__source_file_path}', root=True)
            self.app.system.update()
