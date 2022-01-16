import os
import csv
import ctypes
import platform
import shutil
import sys


class OS:
    __os_release_data = {}

    @classmethod
    def get_release(cls) -> dict:
        if cls.__os_release_data:
            return cls.__os_release_data

        if not os.path.exists('/etc/os-release'):
            return {}

        with open('/etc/os-release') as f:
            reader = csv.reader(f, delimiter="=")
            cls.__os_release_data = {key: value for key, value in reader}

        return cls.__os_release_data

    @classmethod
    def get_release_value(cls, key: str) -> str:
        return cls.get_release().get(key, '')

    @staticmethod
    def is_root() -> bool:
        try:
            return os.getuid() == 0
        except AttributeError:
            pass

        try:
            return ctypes.windll.shell32.IsUserAnAdmin() == 1
        except AttributeError:
            pass

        return False

    @staticmethod
    def platform() -> str:
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

    @staticmethod
    def rm(path: str) -> None:
        if not os.path.exists(path):
            return

        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
        else:
            shutil.rmtree(path)

    @staticmethod
    def root_path() -> str:
        return os.path.abspath(os.sep)

    @classmethod
    def shell(cls) -> str:
        sys_platform = cls.platform()

        if sys_platform == 'windows':
            return os.environ.get('COMSPEC', '')

        return os.environ.get('SHELL', '/bin/sh')

    @classmethod
    def type(cls) -> str:
        sys_platform = cls.platform()

        if sys_platform == 'linux' or sys_platform == 'freebsd':
            # Returns the lowercase operating system name for linux/unix based systems
            # https://www.freedesktop.org/software/systemd/man/os-release.html#ID=
            return cls.get_release_value('ID')

        return sys_platform

    @classmethod
    def type_like(cls) -> str:
        sys_platform = cls.platform()

        if sys_platform == 'linux' or sys_platform == 'freebsd':
            # Return a list identifiers of operating systems that are closely related to the local operating system
            # https://www.freedesktop.org/software/systemd/man/os-release.html#ID_LIKE=
            return cls.get_release_value('ID_LIKE') or cls.get_release_value('ID')

        return sys_platform
