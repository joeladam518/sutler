import click
import os
import shutil
from .os import System


class PosixSystem(System):
    def __init__(self):
        super().__init__()
        self.user.uid = os.getuid(),
        self.user.gid = os.getgid(),
        self.user.gids = tuple(os.getgroups())

    def cp(self, src: str, dst: str, root: bool = False) -> None:
        if root:
            self.exec(f'cp "{src}" "{dst}"', root=True)
        else:
            shutil.copyfile(src, dst, follow_symlinks=True)

    def drop_privileges(self) -> None:
        if not self.is_root():
            # We're not root so, like, whatever dude
            return

        # Reset the uid, guid, and groups back to the user who called this script
        os.setuid(self.user.uid)
        os.setgid(self.user.gid)
        os.setgroups(list(self.user.gids))

        # Ensure a very conservative umask
        # 0o022 == 0755 for directories and 0644 for files
        # 0o027 == 0750 for directories and 0640 for files
        os.umask(0o027)

    def is_root(self) -> bool:
        return os.getuid() == 0

    def mv(self, src: str, dst: str, root: bool = False) -> None:
        if root:
            self.exec(f'mv "{src}" "{dst}"', root=True)
        else:
            shutil.move(src, dst)

    def rename(self, old: str, new: str, root: bool = False) -> None:
        self.mv(old, new, root=root)

    def rm(self, path: str, root: bool = False) -> None:
        if not os.path.exists(path):
            click.ClickException(f'Can not remove "{path}". Path doesn\'t exist.')

        if root:
            if os.path.isfile(path) or os.path.islink(path):
                self.exec(f'rm "{path}"', root=True)
            else:
                self.exec(f'rm -r "{path}"', root=True)
        else:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            else:
                shutil.rmtree(path)
