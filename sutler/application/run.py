import subprocess
import sys
from sutler.application import App


class Run(object):
    @staticmethod
    def command(cmd: str, *args, **kwargs):
        app = App()
        supress_output = kwargs.get('supress_output', False)
        capture_output = False if supress_output else kwargs.get('capture_output', False)
        stdout = subprocess.DEVNULL if supress_output else None
        arguments = [cmd, *args]

        if kwargs.get('root', False):
            arguments.insert(0, 'sudo')

        try:
            completed_process = subprocess.run(
                ' '.join(arguments),
                check=kwargs.get('check', True),
                shell=True,
                executable=app.context.shell,
                stdout=stdout,
                capture_output=capture_output
            )
        except Exception as ex:
            app.drop_privileges()
            raise ex
        else:
            app.drop_privileges()
            if not capture_output:
                return completed_process
            elif completed_process.returncode > 0:
                return completed_process.stderr.decode(sys.getdefaultencoding())
            else:
                return completed_process.stdout.decode(sys.getdefaultencoding())

    @classmethod
    def install(cls, *args):
        app = App()
        if app.os_type() == 'debian':
            cls.command('apt update', root=True)
            cls.command('apt install -y', *args, root=True)
        else:
            raise TypeError('Unsupported os type.')

    @staticmethod
    def script(path: str, *args, **kwargs):
        app = App()
        supress_output = kwargs.get('supress_output', False)
        stdout = subprocess.DEVNULL if supress_output else None
        capture_output = False if supress_output else kwargs.get('capture_output', False)
        arguments = [path, *args]

        if kwargs.get('root', False):
            arguments.insert(0, 'sudo')

        try:
            completed_process = subprocess.run(
                arguments,
                check=kwargs.get('check', True),
                stdout=stdout,
                capture_output=capture_output
            )
        except Exception as ex:
            app.drop_privileges()
            raise ex
        else:
            app.drop_privileges()
            if not capture_output:
                return completed_process
            elif completed_process.returncode > 0:
                return completed_process.stderr.decode(sys.getdefaultencoding())
            else:
                return completed_process.stdout.decode(sys.getdefaultencoding())

    @classmethod
    def uninstall(cls, *args):
        app = App()
        if app.os_type() == 'debian':
            # TODO: Which is the better way?
            # cls.command("apt-get purge -y", *args, root=True)
            # cls.command("apt-get --purge autoremove -y", root=True)
            cls.command('apt purge -y', *args, root=True)
            cls.command('apt autoremove -y', root=True)
        else:
            raise TypeError('Unsupported os type.')
