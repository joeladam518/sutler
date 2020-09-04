import os
import click
import csv
import ctypes
import platform
import subprocess
import sys
from .application import App


def drop_privileges():
    if os.getuid() != 0:
        # We're not root so, like, whatever dude
        return

    app = App()

    # Remove group privileges
    os.setgroups([])

    # Try setting the new uid/gid
    os.setuid(app.context.user.uid)
    os.setgid(app.context.user.gid)

    # Ensure a very conservative umask
    # 0o022 == 0755 for directories and 0644 for files
    # 0o027 == 0750 for directories and 0640 for files
    os.umask(0o027)


def get_linux_distro() -> str:
    return get_linux_release_data()["ID"]


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


def run_cmd():
    click.secho('Run Command!')


def run_script(script, *args, as_root: bool = False) -> int:
    arguments = list(args)
    arguments.insert(0, f"{App().context.get_path('scripts')}/{script}")
    if as_root:
        arguments.insert(0, 'sudo')
    return_code = subprocess.call(arguments)
    drop_privileges()
    if return_code:
        raise subprocess.CalledProcessError(return_code, script)
    return return_code
