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


def drop_privileges():
    if os.getuid() != 0:
        # We're not root so, like, whatever dude
        return

    app = App()

    # Remove group privileges
    os.setgroups([])

    # Try setting the new uid/gid
    os.setgid(app.context.user.gid)
    os.setuid(app.context.user.uid)

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
