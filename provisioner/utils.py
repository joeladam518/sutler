import os
import ctypes
import subprocess
from provisioner.application import App


def bin_path(script=None):
    return App().context.get_path('')


def call_script(script, *args, as_root=False):
    script_path = bin_path(script)
    arguments = list(args)
    arguments.insert(0, script_path)
    if as_root:
        arguments.insert(0, 'sudo')
    subprocess.call(arguments)


def is_root():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin


def is_not_root():
    return not is_root()
