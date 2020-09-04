import click
import getpass
import os
from subprocess import CalledProcessError
from .application import App, Context, User
from .factories import SetupFactory
from .utils import is_root, get_os, run_script


@click.group(invoke_without_command=True)
def cli():
    if is_root():
        raise click.ClickException("You're not allowed to run sutler.sh as root.")
    context = Context()
    context.os = get_os()
    context.set_path('cwd', os.getcwd())
    context.set_path('src', os.path.dirname(os.path.abspath(__file__)))
    context.set_path('templates', f"{context.get_path('src')}/templates")
    context.set_path('scripts', f"{context.get_path('src')}/scripts")
    context.user = User(
        os.getuid(),
        os.getgid(),
        getpass.getuser(),
    )
    App(context=context)


@click.command()
@click.argument('program')
@click.argument('program_arguments', nargs=-1, required=False)
def install(program, program_arguments):
    app = App()

    if not app.validate('program', program):
        raise click.ClickException('Invalid program to install')

    app.context.action = 'install'
    app.context.program = program

    try:
        run_script(f"install-{program}", *program_arguments)
    except CalledProcessError as ex:
        raise click.ClickException(f'{ex.cmd} failed. Return code: {ex.returncode}')


@click.command()
@click.argument('machine_type')
def setup(machine_type):
    app = App()
    app.context.action = 'setup'
    app.context.machine = machine_type

    if not app.validate('os', app.context.os):
        raise click.ClickException('Invalid os type.')
    if not app.validate('machine', app.context.machine):
        raise click.ClickException('Invalid machine type.')

    factory = SetupFactory(app.context.machine)
    provisioner = factory.get_provisioner()
    provisioner.run()


@click.command()
def user():
    app = App()
    app.context.print()


# cli.add_command(install)
cli.add_command(setup)
cli.add_command(user)


if __name__ == '__main__':
    cli()
