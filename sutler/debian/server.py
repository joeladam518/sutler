import click
from ..application import App
from ..utils import run_script


def install():
    app = App()

    click.secho('')
    click.secho(f'I will now install the basic server setup for a {app.context.os} machine.', fg='cyan')

    run_script('cmsg', '-r', 'Hello joel!')
    app.context.print()

    click.secho('Done!', fg='cyan')
    click.secho('')
