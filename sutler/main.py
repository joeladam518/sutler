import click
from .application import App
from .commands import install, setup, uninstall
from .support import Run
from .utils import is_root


@click.group(context_settings={"help_option_names": ['-h', '--help']})
def cli():
    if is_root():
        raise click.ClickException("You're not allowed to run sutler as root.")
    App()


@click.command()
def context():
    app = App()
    app.context.print()


@click.command()
def test():
    Run.command('apt update', root=True)


# noinspection PyTypeChecker
cli.add_command(context)
# noinspection PyTypeChecker
cli.add_command(install)
# noinspection PyTypeChecker
cli.add_command(setup)
# noinspection PyTypeChecker
cli.add_command(test)
# noinspection PyTypeChecker
cli.add_command(uninstall)


if __name__ == '__main__':
    cli()
