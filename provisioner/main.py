import click
from provisioner.app import app
from provisioner.debian import desktop, server


@click.group(invoke_without_command=True)
def cli():
    app.set_user()


@click.command()
@click.argument('machine_type')
@click.option('-o', '--os-type', 'os_type', type=str, default='debian', show_default=True)
def install(machine_type, os_type):
    if os_type not in app.os_types:
        raise click.ClickException('Invalid os type.')

    if machine_type not in app.machine_types:
        raise click.ClickException('Invalid machine type.')

    if machine_type == 'desktop':
        return desktop.install(os_type)
    elif machine_type == 'server':
        return server.install(os_type)


cli.add_command(install)


if __name__ == '__main__':
    cli()
