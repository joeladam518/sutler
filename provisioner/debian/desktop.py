import click


def install(os_type):
    click.secho('')
    click.secho(f'I will now install your {os_type} desktop machine.', fg='cyan')

    click.secho('Done!', fg='cyan')
    click.secho('')
