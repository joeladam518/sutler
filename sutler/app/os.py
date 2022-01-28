import os
import csv
import platform
import subprocess
import sys
from abc import ABC, abstractmethod
from typing import Optional, Union
from getpass import getuser
from .user import User

# Types
CompletedProcess = subprocess.CompletedProcess
RunOutput = Union[CompletedProcess, str]


class Sys:
    """Helper class to gather some os information"""
    __os_release_data = {}

    @classmethod
    def get_os_release(cls) -> dict:
        """
        Get the freedesktop release info. Mainly for linux operating systems.
        https://www.freedesktop.org/software/systemd/man/os-release.html

        In python 3.10 they introduced the 'freedesktop_os_release' function so if
        we have it we use it. But for older versions I've included a polyfill.

        :return: A dict of release information
        :rtype: dict
        """
        if cls.type() not in ['linux', 'freebsd']:
            return {}

        if hasattr(platform, 'freedesktop_os_release'):
            try:
                return platform.freedesktop_os_release()
            except OSError:
                return {}

        # For backward compatibility with older versions of python
        if os.path.exists('/etc/os-release'):
            path = '/etc/os-release'
        elif os.path.exists('/usr/lib/os-release'):
            path = '/usr/lib/os-release'
        else:
            path = None

        if not path:
            return {}

        with open(path) as f:
            reader = csv.reader(f, delimiter="=")
            return {key: value for key, value in reader}

    @classmethod
    def id(cls) -> str:
        """
        Get the operating system's identifier. If not a freedesktop system,
        this will just return the type of system.

        :return: Operating system identifier
        :rtype: str
        """
        system_type = cls.type()

        if system_type in ['linux', 'freebsd']:
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

        if system_type in ['linux', 'freebsd']:
            id_like = cls.release_info('ID_LIKE')

            if not id_like:
                id_ = cls.release_info('ID')
                return (id_,) if id_ else ()

            return tuple(id_like.split(' '))

        return system_type,

    @classmethod
    def name(cls) -> str:
        system_type = cls.type()

        if system_type == 'mac':
            return 'macOS'

        if system_type in ['linux', 'freebsd']:
            return cls.release_info('NAME')

        return platform.system()

    @classmethod
    def release_info(cls, key: Optional[str] = None) -> Union[dict, str]:
        if not cls.__os_release_data:
            cls.__os_release_data = cls.get_os_release()

        if key:
            return cls.__os_release_data.get(key, '')

        return cls.__os_release_data

    @staticmethod
    def root_path() -> str:
        """Get the root path for the system"""
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

        system_type = platform.system().lower()

        if system_type == 'darwin':
            return 'mac'

        return system_type

    @classmethod
    def version(cls) -> str:
        """Get the operating system version"""
        system_type = cls.type()

        if system_type == 'windows':
            return platform.release()

        if system_type == 'mac':
            mac_ver = platform.mac_ver()
            return mac_ver[0]

        return cls.release_info('VERSION_ID')


class System(ABC):
    def __init__(self):
        self.id: str = Sys.id()
        self.id_like: tuple = Sys.id_like()
        self.name: str = Sys.name()
        self.type: str = Sys.type()
        self.user: User = User(getuser(), Sys.shell())

    def __handle_completed_process(self, process: CompletedProcess, capture: bool = False) -> RunOutput:
        self.drop_privileges()

        if capture:
            output = process.stderr if process.returncode > 0 else process.stdout
            return output.decode(sys.getdefaultencoding())

        return process

    @abstractmethod
    def cp(self, src: str, dst: str, root: bool = False) -> None:
        """
        Copy a file

        :param str src: From Path
        :param str dst: To Path
        :param bool root: Run as root
        :return: None
        :rtype: None
        """
        pass

    @abstractmethod
    def drop_privileges(self) -> None:
        """
        Drop any escalated privileges

        TODO: This function might not be needed. It seems like if I use subprocess and only escalate the
              user's privileges during those individual subprocess calls I won't escalate sutler's privileges...
              Maybe... Keeping it around just in case and until I'm sure I don't need it.

        :return: None
        :rtype: None
        """
        pass

    def exec(self, cmd: str, *args, **kwargs) -> RunOutput:
        """
        Execute a command

        :param str cmd: The command
        :param args: The command's arguments
        :param kwargs: The command's arguments (using keys)
        :return: The command's output
        :rtype: RunOutput
        """
        arguments = [cmd, *args]
        supress_output = kwargs.get('supress_output', False)
        capture_output = False if supress_output else kwargs.get('capture_output', False)
        stdout = subprocess.DEVNULL if supress_output else None

        if kwargs.get('root', False):
            arguments.insert(0, 'sudo')

        try:
            process = subprocess.run(
                ' '.join(arguments),
                check=kwargs.get('check', True),
                shell=True,
                executable=self.user.shell,
                stdout=stdout,
                capture_output=capture_output,
                env=kwargs.get('env', None)
            )
        except Exception as ex:
            self.drop_privileges()
            raise ex
        else:
            return self.__handle_completed_process(process, capture_output)

    def exec_script(self, path: str, *args, **kwargs) -> RunOutput:
        """
        Run a script

        :param str path: The path to the script to run
        :param args: The script's arguments
        :param kwargs: The script's arguments (using keys)
        :return: The script's output
        :rtype: RunOutput
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"'{path}' was not found.")

        arguments = [path, *args]
        supress_output = kwargs.get('supress_output', False)
        capture_output = False if supress_output else kwargs.get('capture_output', False)
        stdout = subprocess.DEVNULL if supress_output else None

        if kwargs.get('root', False):
            arguments.insert(0, 'sudo')

        try:
            process = subprocess.run(
                arguments,
                check=kwargs.get('check', True),
                stdout=stdout,
                capture_output=capture_output,
                env=kwargs.get('env', None)
            )
        except Exception as ex:
            self.drop_privileges()
            raise ex
        else:
            return self.__handle_completed_process(process, capture_output)

    @abstractmethod
    def is_root(self) -> bool:
        """
        Determine if sutler is running as root

        :return: bool
        :rtype: bool
        """
        pass

    @abstractmethod
    def mv(self, src: str, dst: str, root: bool = False) -> None:
        """
        Move a file

        :param str src: From Path
        :param str dst: To Path
        :param bool root: Run as root
        :return: The completed process
        :rtype: None
        """
        pass

    @abstractmethod
    def rename(self, old: str, new: str, root: bool = False) -> None:
        """
        Rename a file

        :param str old: Old file name
        :param str new: New file name
        :param bool root: Run as root
        :return: The completed process
        :rtype: None
        """
        pass

    @abstractmethod
    def rm(self, path: str, root: bool = False) -> None:
        """
        Remove a file

        :param str path: file path
        :param bool root: Run as root
        :return: None
        :rtype: None
        """
        pass
