import os
from git import Repo
from .installer import Installer


class FzfInstaller(Installer):
    def install(self) -> None:
        fzf_dir = os.path.join(self.app.user.home, '.fzf')
        install_script_path = os.path.join(fzf_dir, 'install')

        if not os.path.isdir(fzf_dir):
            Repo.clone_from("https://github.com/junegunn/fzf.git", fzf_dir, depth=1)

        if not os.path.exists(install_script_path):
            self.ctx.fail("Could not find fzf's install script")

        self.app.sys.exec_script(install_script_path)

    def uninstall(self) -> None:
        fzf_dir = os.path.join(self.app.user.home, '.fzf')
        uninstall_script_path = os.path.join(fzf_dir, 'uninstall')

        if not os.path.exists(uninstall_script_path):
            self.ctx.fail("Could not find fzf's uninstall script")

        self.app.sys.exec_script(uninstall_script_path)
        self.app.sys.rm(fzf_dir)
