import click
from click.core import Context as ClickContext
from .application import App
from .commands import install, setup, uninstall
from .commands import context, test


@click.group(context_settings={"help_option_names": ['-h', '--help']})
@click.pass_context
def cli(ctx: ClickContext):
    app = ctx.ensure_object(App)
    if app.is_root():
        ctx.fail("You're not allowed to run sutler as root")
    if app.os_type() != 'debian':
        ctx.fail("Sorry, currently sutler only supports Debian based systems")


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
