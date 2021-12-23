import os
from git import Repo
from ..support import Run
from .installer import Installer


class FzfInstaller(Installer):
    def install(self):
        home_dir = self.app.context.user.home
        os.chdir(home_dir)

        if not os.path.isdir(f'{home_dir}/.fzf'):
            Repo.clone_from("https://github.com/junegunn/fzf.git", f'{home_dir}/.fzf', depth=1)

        Run.script(f"{home_dir}/.fzf/install")

    def uninstall(self):
        home_dir = self.app.context.user.home
        os.chdir(home_dir)

        if not os.path.exists(f'{home_dir}/.fzf/uninstall'):
            self.ctx.fail('Could not find fzf\'s uninstall script.')
            return

        Run.script(f"{home_dir}/.fzf/uninstall")
