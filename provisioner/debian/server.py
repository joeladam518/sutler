import click


def install(os_type):
    click.secho('')
    click.secho(f'I will now install the basic server setup for a {os_type} machine.', fg='cyan')

    click.secho('Done!', fg='cyan')
    click.secho('')
