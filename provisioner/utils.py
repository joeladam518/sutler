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


def exec_script(script, *args):
    script_path = bin_path(script)
    arguments = list(args)
    arguments_format_specifiers = ""

    for i in range(len(arguments)):
        arguments[i] = str(args[i])
        arguments_format_specifiers = f'{arguments} %s'

    print(f"{script_path} {arguments_format_specifiers}" % tuple(arguments))


def is_root():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin


def is_not_root():
    return not is_root()
