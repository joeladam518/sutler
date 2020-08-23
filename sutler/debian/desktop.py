import click
from ..application import App


def install():
    app = App()

    click.secho('')
    click.secho(f'I will now install your {app.context.os} desktop machine.', fg='cyan')

    click.secho('Done!', fg='cyan')
    click.secho('')
