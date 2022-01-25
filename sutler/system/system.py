import os
import subprocess
import sys
from abc import ABC, abstractmethod
from getpass import getuser
from typing import Union
from .base import Sys
from .user import User

# Types
CompletedProcess = subprocess.CompletedProcess
RunOutput = Union[CompletedProcess, str]


class System(ABC):
    def __init__(self):
        self.id: str = Sys.id()
        self.id_like: tuple = Sys.id_like()
        self.name: str = Sys.name()
        self.type: str = Sys.type()
        self.user: User = User(getuser(), Sys.shell())

    def __handle_completed_process(self, process: CompletedProcess, capture: bool = False):
        self.drop_privileges()
        if not capture:
            return process
        else:
            output = process.stderr if process.returncode > 0 else process.stdout
            return output.decode(sys.getdefaultencoding())

    @abstractmethod
    def cp(self, fp: str, tp: str, root: bool = False):
        """
        Copy a file

        :param str fp: From Path
        :param str tp: To Path
        :param bool root: Run as root
        :return: CompletedProcess
        :rtype: CompletedProcess
        """
        pass

    @abstractmethod
    def drop_privileges(self):
        """
        Drop any escalated privileges

        TODO: This function might not be needed. It seems like if I use subprocess and only escalate the
              user's privileges during those individual subprocess calls I won't escalate sutler's privileges...
              Maybe... Keeping it around just in case and until I'm sure I don't need it.
              Additionally I'm pretty sure this will only work for posix based systems...

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
    def mv(self, fp: str, tp: str, root: bool = False):
        """
        Move a file

        :param str fp: From Path
        :param str tp: To Path
        :param bool root: Run as root
        :return: The completed process
        :rtype: CompletedProcess
        """
        pass

    @abstractmethod
    def rename(self, old: str, new: str, root: bool = False):
        """
        Rename a file

        :param str old: Old file name
        :param str new: New file name
        :param bool root: Run as root
        :return: The completed process
        :rtype: CompletedProcess
        """
        pass

    @abstractmethod
    def rm(self, path: str, root: bool = False):
        """
        Remove a file

        :param str path: file path
        :param bool root: Run as root
        :return: None
        :rtype: None
        """
        pass
