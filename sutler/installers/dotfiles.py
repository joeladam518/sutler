import os
from git import Repo
from .installer import Installer


class DotfilesInstaller(Installer):
    def install(self, system: str) -> None:
        home_dir = self.app.user.home
        repos_dir = os.path.join(home_dir, 'repos')
        dotfiles_dir = os.path.join(repos_dir, 'dotfiles')
        install_script_path = os.path.join(dotfiles_dir, 'install.sh')
        os.chdir(home_dir)

        if not os.path.isdir(repos_dir):
            os.mkdir(repos_dir, 0o755)

        if not os.path.isdir(dotfiles_dir):
            if system == 'desktop':
                Repo.clone_from('git@github.com:joeladam518/dotfiles.git', dotfiles_dir, depth=1)
            else:
                Repo.clone_from('https://github.com/joeladam518/dotfiles.git', dotfiles_dir, depth=1)

        if not os.path.exists(install_script_path):
            self.ctx.fail('Failed to install dotfiles. Could not find the install script')

        self.app.system.exec_script(install_script_path, system)

    def uninstall(self, system: str) -> None:
        home_dir = self.app.user.home
        repos_dir = os.path.join(home_dir, 'repos')
        dotfiles_dir = os.path.join(repos_dir, 'dotfiles')
        uninstall_script_path = os.path.join(dotfiles_dir, 'uninstall.sh')
        os.chdir(home_dir)

        if not os.path.exists(uninstall_script_path):
            self.ctx.fail('Failed to uninstall dotfiles. Could not find the uninstall script')

        self.app.system.exec_script(uninstall_script_path, system)
        self.app.system.rm(dotfiles_dir)
