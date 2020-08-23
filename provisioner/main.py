import click
import os
from subprocess import CalledProcessError
from .application import App, Context
from .debian import desktop, server
from .utils import is_root, run_script


@click.group(invoke_without_command=True)
def cli():
    if is_root():
        raise click.ClickException("You're not allowed to run provisioner as root.")
    context = Context()
    context.set_path('cwd', os.getcwd())
    context.set_path('src', os.path.dirname(os.path.abspath(__file__)))
    context.set_path('templates', f"{context.get_path('src')}/templates")
    context.set_path('scripts', f"{context.get_path('src')}/scripts")
    App(context=context)


@click.command()
@click.argument('program')
@click.argument('program_arguments', nargs=-1, required=False)
def install(program, program_arguments):
    app = App()

    if not app.validate('program', program):
        raise click.ClickException('Invalid program to install')

    app.context.action = 'install'
    app.context.program = f"install-{program}"

    try:
        run_script(app.context.program, * program_arguments)
    except CalledProcessError as ex:
        raise click.ClickException(f'failed to run {ex.cmd}. return code {ex.returncode}')


@click.command()
@click.argument('machine_type')
@click.option('-o', '--os-type', 'os_type', required=False, type=str, default='ubuntu', show_default=True)
def setup(machine_type, os_type):
    app = App()
    app.context.action = 'setup'
    if not app.validate('machine', machine_type):
        raise click.ClickException('Invalid machine type.')
    app.context.machine = machine_type
    if not app.validate('os', os_type):
        raise click.ClickException('Invalid os type.')
    app.context.os = os_type

    # app.context.print()
    if machine_type == 'server':
        return server.install()
    elif machine_type == 'desktop':
        return desktop.install()


@click.command()
def user():
    app = App()
    app.context.print()


cli.add_command(install)
cli.add_command(setup)
cli.add_command(user)


if __name__ == '__main__':
    cli()
