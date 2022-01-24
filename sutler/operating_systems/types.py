import click
import os
import shutil
import subprocess
import sys
from abc import ABC
from typing import TYPE_CHECKING, Union
from ..support import OS

if TYPE_CHECKING:
    from ..application import App

# Types
CompletedProcess = subprocess.CompletedProcess
RunOutput = Union[CompletedProcess, str]


def handle_completed_process(process: CompletedProcess, capture_output: bool) -> RunOutput:
    if not capture_output:
        return process
    elif process.returncode > 0:
        return process.stderr.decode(sys.getdefaultencoding())
    else:
        return process.stdout.decode(sys.getdefaultencoding())


# TODO: Add a WindowsSystem Abstract Base Class (ABC)


class PosixSystem(ABC):
    """
    Posix system helper class

    app : App
        The operating system type. For a posix systems, this will return the operating system's name.
        example: 'ubuntu', 'raspbian', 'arch', 'fedora', debian. etc... But, for window and mac it will just
        return 'windows' or 'mac'
    """

    def __init__(self, app: 'App'):
        self.app: 'App' = app

    def cp(self, fp: str, tp: str, root: bool = False) -> CompletedProcess:
        """
        Copy a file

        :param str fp: From Path
        :param str tp: To Path
        :param bool root: Run as root
        :return: CompletedProcess
        :rtype: CompletedProcess
        """
        return self.exec(f'cp "{fp}" "{tp}"', root=root)

    def drop_privileges(self) -> None:
        """
        Drop any escalated privileges

        TODO: This function might not be needed. It seems like if I use subprocess and only escalate the
              user's privileges during those individual subprocess calls I won't escalate sutler's privileges...
              Maybe... Keeping it around just in case and until I'm sure I don't need it.
              Additionally I'm pretty sure this will only work for posix based systems...

        :return: None
        :rtype: None
        """
        if not OS.is_root():
            # We're not root so, like, whatever dude
            return

        # Reset the uid, guid, and groups back to the user who called this script
        os.setuid(self.app.user.uid)
        os.setgid(self.app.user.gid)
        os.setgroups(list(self.app.user.gids))

        # Ensure a very conservative umask
        # 0o022 == 0755 for directories and 0644 for files
        # 0o027 == 0750 for directories and 0640 for files
        os.umask(0o027)

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
            proc = subprocess.run(
                ' '.join(arguments),
                check=kwargs.get('check', True),
                shell=True,
                executable=self.app.user.shell,
                stdout=stdout,
                capture_output=capture_output,
                env=kwargs.get('env', None)
            )
        except Exception as ex:
            self.drop_privileges()
            raise ex
        else:
            self.drop_privileges()
            return handle_completed_process(proc, capture_output)

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
            proc = subprocess.run(
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
            self.drop_privileges()
            return handle_completed_process(proc, capture_output)

    def mv(self, fp: str, tp: str, root: bool = False) -> CompletedProcess:
        """
        Move a file

        :param str fp: From Path
        :param str tp: To Path
        :param bool root: Run as root
        :return: The completed process
        :rtype: CompletedProcess
        """
        return self.exec(f'mv "{fp}" "{tp}"', root=root)

    def rm(self, path: str, root: bool = False) -> None:
        """
        Remove a file

        :param str path: file path
        :param bool root: Run as root
        :return: None
        :rtype: None
        """
        if not os.path.exists(path):
            click.ClickException(f'Can not remove "{path}". Path doesn\'t exist.')

        if os.path.isfile(path) or os.path.islink(path):
            if root:
                self.exec(f'rm "{path}"', root=True)
            else:
                os.unlink(path)
        else:
            if root:
                self.exec(f'rm -r "{path}"', root=True)
            else:
                shutil.rmtree(path)

    def rename(self, old: str, new: str, root: bool = False) -> CompletedProcess:
        """
        Move a file. (proxy for mv)

        :param str old: Old file name
        :param str new: New file name
        :param bool root: Run as root
        :return: The completed process
        :rtype: CompletedProcess
        """
        return self.mv(old, new, root=root)
