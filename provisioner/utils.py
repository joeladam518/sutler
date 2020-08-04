import os
import ctypes
import subprocess


dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def bin_path(script=None):
    path = f'{dir_path}/bin'
    if not script:
        return path

    script_path = f'{path}/{script}'

    if not os.path.exists(script_path):
        raise FileExistsError(f'"{script_path}" was not found.')

    return script_path


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
