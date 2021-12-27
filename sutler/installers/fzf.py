import os
from git import Repo
from ..application import Run
from ..support import OS
from .installer import Installer


class FzfInstaller(Installer):
    def install(self) -> None:
        fzf_dir = os.path.join(self.app.context.user.home, '.fzf')
        install_script_path = os.path.join(fzf_dir, 'install')

        if not os.path.isdir(fzf_dir):
            Repo.clone_from("https://github.com/junegunn/fzf.git", fzf_dir, depth=1)

        if not os.path.exists(install_script_path):
            self.ctx.fail("Could not find fzf's install script")

        Run.script(install_script_path)

    def uninstall(self) -> None:
        fzf_dir = os.path.join(self.app.context.user.home, '.fzf')
        uninstall_script_path = os.path.join(fzf_dir, 'uninstall')

        if not os.path.exists(uninstall_script_path):
            self.ctx.fail("Could not find fzf's uninstall script")

        Run.script(uninstall_script_path)
        OS.rm(fzf_dir)
