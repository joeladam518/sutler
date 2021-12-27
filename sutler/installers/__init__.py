# -*- coding: utf-8 -*-
from .composer import ComposerInstaller
from .dotfiles import DotfilesInstaller
from .fzf import FzfInstaller
from .mariadb import MariadbInstaller
from .nginx import NginxInstaller
from .node import NodeInstaller
from .php import PhpInstaller
from .redis import RedisInstaller
from .sumblime import SublimeInstaller

__all__ = [
    'ComposerInstaller',
    'DotfilesInstaller',
    'FzfInstaller',
    'MariadbInstaller',
    'NginxInstaller',
    'NodeInstaller',
    'PhpInstaller',
    'RedisInstaller',
    'SublimeInstaller'
]
