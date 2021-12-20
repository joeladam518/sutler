import click
from .application import App
from .commands import install, setup, uninstall
from .support import Version
from .utils import is_root


@click.group(context_settings={"help_option_names": ['-h', '--help']})
def cli():
    if is_root():
        raise click.ClickException("You're not allowed to run sutler as root.")
    else:
        App()


@click.command()
def context():
    app = App()
    app.context.print()


@click.command()
def test():
    print(str(Version((8, 1)) == Version('8.1.0')))
    # print(Version('7.4'))


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
