import os
import subprocess
import sys
from typing import Union
from sutler.application import App

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


class Run(object):
    @staticmethod
    def command(cmd: str, *args, **kwargs) -> RunOutput:
        app = App()
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
                executable=app.context.shell,
                stdout=stdout,
                capture_output=capture_output,
                env=kwargs.get('env', None)
            )
        except Exception as ex:
            app.drop_privileges()
            raise ex
        else:
            app.drop_privileges()
            return handle_completed_process(proc, capture_output)

    @classmethod
    def install(cls, *args) -> None:
        app = App()
        if app.os_type() == 'debian':
            cls.command('apt update', root=True)
            cls.command('apt install -y', *args, root=True)
        else:
            raise TypeError('Unsupported os type.')

    @staticmethod
    def script(path: str, *args, **kwargs) -> RunOutput:
        if not os.path.exists(path):
            raise FileNotFoundError(f"'{path}' was not found.")

        app = App()
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
            app.drop_privileges()
            raise ex
        else:
            app.drop_privileges()
            return handle_completed_process(proc, capture_output)

    @classmethod
    def uninstall(cls, *args) -> None:
        app = App()
        if app.os_type() == 'debian':
            # TODO: Which is the better way?
            # cls.command("apt-get purge -y", *args, root=True)
            # cls.command("apt-get --purge autoremove -y", root=True)
            cls.command('apt purge -y', *args, root=True)
            cls.command('apt autoremove -y', root=True)
        else:
            raise TypeError('Unsupported os type.')

    @classmethod
    def update_and_upgrade(cls):
        app = App()
        if app.os_type() == 'debian':
            env = os.environ.copy()
            env['DEBIAN_FRONTEND'] = 'noninteractive'
            cls.command('apt update', root=True)
            cls.command('apt upgrade -y', root=True, env=env)
            cls.command('apt autoremove -y', root=True)
        else:
            raise TypeError('Unsupported os type.')
