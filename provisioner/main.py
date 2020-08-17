import click
import os
from .application import App, Context
from .debian import desktop, server
from .utils import is_root


@click.group(invoke_without_command=True)
def cli():
    if is_root():
        raise click.ClickException("You're not allowed to run provisioner as root.")
    context = Context()
    context.set_path('cwd', os.getcwd())
    context.set_path('src', os.path.dirname(os.path.abspath(__file__)))
    context.set_path('templates', f"{context.get_path('src')}/templates")
    App(context=context)


@click.command()
@click.argument('program')
@click.argument('program_arguments', nargs=-1, required=False)
def install(program, program_arguments):
    pass
    # app = App()
    # if app.is_valid_type('program', program):
    #     raise click.ClickException('Invalid program to install')
    #
    # app.print_user()
    #
    # call_script(f'install-{program}', *program_arguments)


@click.command()
@click.argument('machine_type')
@click.option('-o', '--os-type', 'os_type', required=False, type=str, default='debian', show_default=True)
def setup(machine_type, os_type):
    pass
    # app = App()
    # if app.is_valid_type('machine', machine_type):
    #     raise click.ClickException('Invalid machine type.')
    #
    # if app.is_valid_type('os', os_type):
    #     raise click.ClickException('Invalid os type.')
    #
    # if machine_type == 'server':
    #     return server.install(os_type)
    # elif machine_type == 'desktop':
    #     return desktop.install(os_type)


@click.command()
def user():
    app = App()
    app.context.print()


cli.add_command(install)
cli.add_command(setup)
cli.add_command(user)


if __name__ == '__main__':
    cli()
