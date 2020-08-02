import click
from provisioner.debian.installer import Installer


@click.group(invoke_without_command=True)
def cli():
    pass


@click.command()
@click.argument('machine_type')
@click.option('-o', '--os-type', 'os_type', type=str, default='debian', show_default=True)
@click.option('-v', '--verbose', 'verbose', count=True)
def install(machine_type, os_type, verbose):
    click.secho('Install command called!', fg='cyan')
    click.echo(f'machine_type: {machine_type}')
    click.echo(f'     os_type: {os_type}')
    click.echo(f'     verbose: {verbose}')
    click.echo()

    installer = Installer(machine_type, os_type)
    installer.validate()
    installer.install()


cli.add_command(install)


if __name__ == '__main__':
    cli()
