import os
import click
import csv
import ctypes
import platform
import sys


def confirm(question: str, default: bool = False, fg: str = None) -> bool:
    tries = 2
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    prompt = " [y/N] "

    while tries > 0:
        if fg:
            click.secho(question + prompt, nl=False, fg=fg)
            choice = input().lower()
        else:
            choice = input(question + prompt).lower()

        if choice in valid:
            return valid[choice]

        tries = tries - 1

        if tries > 0:
            click.secho("Please enter 'yes' or 'no'", fg='yellow')

    return default


def get_distro() -> str:
    return get_os_release_value('ID')


def get_distro_like() -> str:
    return get_os_release_value('ID_LIKE')


def get_os() -> str:
    system = get_platform()

    if system == 'linux':
        return get_distro()

    return system


def get_os_like() -> str:
    system = get_platform()

    if system == 'linux':
        return get_distro_like()

    return system


def get_os_release() -> dict:
    if not os.path.exists('/etc/os-release'):
        return {}

    with open('/etc/os-release') as f:
        reader = csv.reader(f, delimiter="=")
        data = {key: value for key, value in reader}

    return data


def get_os_release_value(key: str) -> str:
    return get_os_release().get(key, '')


def get_platform() -> str:
    if sys.platform in ['win32', 'win64', 'cygwin']:
        return 'windows'

    if sys.platform == 'darwin':
        return 'mac'

    if sys.platform == 'linux':
        return 'linux'

    system = platform.system().lower()

    if system == 'darwin':
        return 'mac'

    return system


def is_root() -> bool:
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin
