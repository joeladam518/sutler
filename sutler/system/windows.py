import click
import ctypes
import os
import shutil
from .base import System


class WindowsSystem(System):
    def cp(self, src: str, dst: str, root: bool = False) -> None:
        # TODO: copy with elevated privileges
        shutil.copyfile(src, dst)

    def drop_privileges(self) -> None:
        # TODO: How do you drop privileges on a windows machine?
        pass

    def is_root(self) -> bool:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

    def mv(self, src: str, dst: str, root: bool = False) -> None:
        # TODO: move with elevated privileges
        shutil.move(src, dst)

    def rename(self, old: str, new: str, root: bool = False) -> None:
        self.mv(old, new, root=root)

    def rm(self, path: str, root: bool = False) -> None:
        if not os.path.exists(path):
            click.ClickException(f'Can not remove "{path}". Path doesn\'t exist.')

        # TODO: move with elevated privileges
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
        else:
            shutil.rmtree(path)
