# -*- coding: utf-8 -*-
from .install import install
from .setup import setup
from .test import context, test
from .uninstall import uninstall

__all__ = [
    'context',
    'install',
    'setup',
    'test',
    'uninstall',
]
