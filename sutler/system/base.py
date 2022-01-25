import os
import csv
import platform
import sys
from typing import Optional, Union


def get_os_release_path() -> Optional[str]:
    if os.path.exists('/etc/os-release'):
        return '/etc/os-release'

    if os.path.exists('/usr/lib/os-release'):
        return '/usr/lib/os-release'

    return None


def get_os_release() -> dict:
    if hasattr(platform, 'freedesktop_os_release'):
        try:
            return platform.freedesktop_os_release()
        except OSError:
            return {}

    # for backward compatibility with older versions of python
    path = get_os_release_path()

    if not path:
        return {}

    with open(path) as f:
        reader = csv.reader(f, delimiter="=")
        return {key: value for key, value in reader}


class Sys:
    __os_release_data = {}

    @classmethod
    def id(cls) -> str:
        """Get the operating system's identifier"""
        system_type = cls.type()

        if system_type == 'mac':
            return 'macos'

        if system_type == 'linux' or system_type == 'freebsd':
            # Returns the lowercase operating system name for linux/freebsd based systems
            # https://www.freedesktop.org/software/systemd/man/os-release.html#ID=
            return cls.release_info('ID')

        return system_type

    @classmethod
    def id_like(cls) -> tuple:
        """
        The operating systems that the the local operating system is based on. If not a freedesktop system,
        this will just return the type of system.

        https://www.freedesktop.org/software/systemd/man/os-release.html#ID_LIKE=

        :return: Tuple of operating systems that are closely related to the local operating system.
        :rtype: tuple
        """
        system_type = cls.type()

        if system_type == 'linux' or system_type == 'freebsd':
            id_like = cls.release_info('ID_LIKE')
            if id_like:
                return tuple(id_like.split(' '))

            return cls.release_info('ID'),

        return system_type,

    @classmethod
    def name(cls):
        system_type = cls.type()

        if system_type == 'mac':
            return 'macOS'

        if system_type == 'linux' or system_type == 'freebsd':
            # Returns the lowercase operating system name for linux/freebsd based systems
            # https://www.freedesktop.org/software/systemd/man/os-release.html#ID=
            return cls.release_info('NAME')

        return platform.system()

    @classmethod
    def release_info(cls, key: Optional[str] = None) -> Union[dict, str]:
        if not cls.__os_release_data:
            cls.__os_release_data = get_os_release()

        return cls.__os_release_data.get(key, '') if key else cls.__os_release_data

    @classmethod
    def release_version(cls) -> Optional[str]:
        system_type = cls.type()

        if system_type == 'windows':
            return platform.release()

        if system_type == 'mac':
            mac_ver = platform.mac_ver()
            return mac_ver[0]

        if system_type == 'linux' or system_type == 'freebsd':
            # Returns the lowercase operating system name for linux/freebsd based systems
            # https://www.freedesktop.org/software/systemd/man/os-release.html#ID=
            return cls.release_info('VERSION_ID')

        return None

    @staticmethod
    def root_path() -> str:
        return os.path.abspath(os.sep)

    @classmethod
    def shell(cls) -> str:
        """Get the current default shell"""
        if cls.type() == 'windows':
            return os.environ.get('COMSPEC', '')

        return os.environ.get('SHELL', '/bin/sh')

    @staticmethod
    def type() -> str:
        """Get the type of operating system"""
        if sys.platform in ['win32', 'win64', 'cygwin']:
            return 'windows'

        if sys.platform == 'darwin':
            return 'mac'

        if sys.platform == 'linux':
            return 'linux'

        name = platform.system().lower()

        if name == 'darwin':
            return 'mac'

        return name
