import shutil
from ..application import App


def installed(program: str) -> bool:
    """Checks is a program is installed.
    NOTE: Works in most cases, but not in every case. Doesn't recognize jetbrains programs.
          It's also finicky, you need to know the exact name of the command or package.

    :param str program: The program name to check
    :return: Boolean indicating weather or not the program is installed
    :rtype: bool
    """
    return is_cmd_installed(program) or is_pkg_installed(program)


def is_cmd_installed(program: str) -> bool:
    return shutil.which(program) is not None


def is_pkg_installed(program: str) -> bool:
    app = App()
    proc = app.os.exec(f"dpkg -l | grep -E '^ii' | grep -iwq '{program}'", check=False)
    return proc.returncode == 0
