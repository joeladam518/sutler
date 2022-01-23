import click
from click.core import Context as ClickContext
from .application import App
from .commands import install, setup, uninstall
from .commands import test


@click.group(invoke_without_command=True, context_settings={"help_option_names": ['-h', '--help']})
@click.pass_context
def cli(ctx: ClickContext):
    app = ctx.ensure_object(App)
    if app.is_root():
        ctx.fail("You're not allowed to run sutler as root")
    if app.system.type_like not in ['ubuntu debian', 'debian']:
        ctx.fail("Sorry, currently sutler only supports Debian based systems")
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# noinspection PyTypeChecker
cli.add_command(setup)
# noinspection PyTypeChecker
cli.add_command(install)
# noinspection PyTypeChecker
cli.add_command(uninstall)
# noinspection PyTypeChecker
cli.add_command(test)


if __name__ == '__main__':
    cli()
