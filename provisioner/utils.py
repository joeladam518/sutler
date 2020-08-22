import os
import click
import ctypes
import subprocess
from provisioner.application import App


def run_cmd():
    click.secho('Run Command!')


def run_script(script, *args, as_root: bool = False):
    arguments = list(args)
    arguments.insert(0, script)
    if as_root:
        arguments.insert(0, 'sudo')
    return_code = subprocess.call(arguments)
    drop_privileges()
    if return_code:
        raise subprocess.CalledProcessError(return_code, script)
    return return_code


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


def is_root() -> bool:
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


def is_not_root() -> bool:
    return not is_root()
