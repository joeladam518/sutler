# -*- coding: utf-8 -*-
from .composer import ComposerInstaller
from .dotfiles import DotfilesInstaller
from .fzf import FzfInstaller
from .mariadb import MariadbInstaller
from .node import NodeInstaller
from .php import PhpInstaller
from .redis import RedisInstaller

__all__ = [
    'ComposerInstaller',
    'DotfilesInstaller',
    'FzfInstaller',
    'MariadbInstaller',
    'NodeInstaller',
    'PhpInstaller',
    'RedisInstaller'
]
