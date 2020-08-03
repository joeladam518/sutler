import click
from provisioner.debian import desktop, server
from provisioner.config import os_types, machine_types
from provisioner.utils import is_not_root

# TODO: id your going to call this as root
@click.group(invoke_without_command=True)
def cli():
    if is_not_root():
        raise click.ClickException('Provisioner must be run with administrator privileges.')


@click.command()
@click.argument('machine_type')
@click.option('-o', '--os-type', 'os_type', type=str, default='debian', show_default=True)
def install(machine_type, os_type):
    if os_type not in os_types:
        raise click.ClickException('Invalid os type.')

    if machine_type not in machine_types:
        raise click.ClickException('Invalid machine type.')

    if machine_type == 'desktop':
        return desktop.install(os_type)
    elif machine_type == 'server':
        return server.install(os_type)

    exit()


cli.add_command(install)


if __name__ == '__main__':
    cli()
