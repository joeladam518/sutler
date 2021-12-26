import os
from git import Repo
from ..application import Run
from .installer import Installer
from ..support import OS


class DotfilesInstaller(Installer):
    def install(self, system: str) -> None:
        home_dir = self.app.context.user.home
        repos_dir = os.path.join(home_dir, 'repos')
        dotfiles_dir = os.path.join(repos_dir, 'dotfiles')
        install_script_path = os.path.join(dotfiles_dir, 'install.sh')
        os.chdir(home_dir)

        if not os.path.isdir(repos_dir):
            os.mkdir(repos_dir, 0o755)

        if not os.path.isdir(dotfiles_dir):
            Repo.clone_from("https://github.com/joeladam518/dotfiles.git", dotfiles_dir, depth=1)

        if not os.path.exists(install_script_path):
            self.ctx.fail('Failed to install dotfiles. Could not find the install script')

        Run.script(install_script_path, system)

    def uninstall(self, system: str) -> None:
        home_dir = self.app.context.user.home
        repos_dir = os.path.join(home_dir, 'repos')
        dotfiles_dir = os.path.join(repos_dir, 'dotfiles')
        uninstall_script_path = os.path.join(dotfiles_dir, 'uninstall.sh')
        os.chdir(home_dir)

        if not os.path.exists(uninstall_script_path):
            self.ctx.fail('Failed to uninstall dotfiles. Could not find the uninstall script')

        Run.script(uninstall_script_path, system)
        OS.rm(dotfiles_dir)
