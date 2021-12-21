import click
from .application import App
from .commands import install, setup, uninstall
from .commands import context, test
from .utils import is_root


@click.group(context_settings={"help_option_names": ['-h', '--help']})
@click.pass_context
def cli(ctx):
    if is_root():
        raise click.ClickException("You're not allowed to run sutler as root.")
    ctx.ensure_object(dict)
    ctx.obj['app'] = App()


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
