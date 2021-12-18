import subprocess
import sys
from ..application import App


class Run(object):
    @staticmethod
    def command(cmd: str, *args, **kwargs):
        app = App()
        capture_output = bool(kwargs.get('capture_output', False))
        arguments = [cmd, *args]

        if bool(kwargs.get('root', False)):
            arguments.insert(0, 'sudo')

        try:
            completed_process = subprocess.run(
                ' '.join(arguments),
                check=True,
                shell=True,
                executable=app.context.shell,
                capture_output=capture_output
            )
        except Exception as ex:
            app.drop_privileges()
            raise ex
        else:
            app.drop_privileges()
            if capture_output:
                return completed_process.stdout.decode(sys.getdefaultencoding())
            else:
                return completed_process

    @staticmethod
    def script(name: str, *args, **kwargs):
        app = App()
        capture_output = bool(kwargs.get('capture_output', False))
        arguments = [f"{app.context.get_path('scripts')}/{name}", *args]

        if bool(kwargs.get('root', False)):
            arguments.insert(0, 'sudo')

        try:
            completed_process = subprocess.run(
                arguments,
                check=True,
                capture_output=capture_output
            )
        except Exception as ex:
            app.drop_privileges()
            raise ex
        else:
            app.drop_privileges()
            if capture_output:
                return completed_process.stdout.decode(sys.getdefaultencoding())
            else:
                return completed_process
