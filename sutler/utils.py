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


def get_linux_distro() -> str:
    return get_linux_release_data().get('ID')


def get_linux_release_data() -> dict:
    release_data = {}
    with open("/etc/os-release") as f:
        reader = csv.reader(f, delimiter="=")
        for row in reader:
            if row:
                release_data[row[0]] = row[1]

    return release_data


def get_os() -> str:
    if sys.platform == 'darwin':
        return 'mac'

    if sys.platform == 'linux':
        return get_linux_distro()

    if sys.platform in ['win32', 'win64', 'cygwin']:
        return 'windows'

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
