from ..application import Run
from ..helpers import installed
from .installer import Installer


class SublimeInstaller(Installer):
    __source = 'deb https://download.sublimetext.com/ apt/stable/'
    __source_file_path = '/etc/apt/sources.list.d/sublime-text.list'

    def install(self, program: str) -> None:
        if program not in ('text', 'merge'):
            self.ctx.fail("Error: Invalid program name. Valid values are {text|merge}.")

        Run.command('wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -')
        Run.command(f'echo "{self.__source}" | sudo tee {self.__source_file_path}', root=True)
        Run.update()
        Run.install(f'sublime-{program}')

    def uninstall(self, program: str) -> None:
        if program not in ('text', 'merge'):
            self.ctx.fail("Error: Invalid program name. Valid values are {text|merge}.")

        Run.uninstall(f'sublime-{program}')

        if not installed('sublime-text') and not installed('sublime-merge'):
            Run.command(f'rm {self.__source_file_path}', root=True)
            Run.update()
