import click
from click.core import Context as ClickContext
from ..application import App


@click.command()
@click.pass_context
def context(ctx: ClickContext):
    app: App = ctx.find_root().obj
    app.context.print()
    click.secho("Paths", fg='cyan')
    click.secho(f"base_path", nl=False, fg='white')
    click.secho(f": {app.path()}")
    click.secho(f"scripts_path", nl=False, fg='white')
    click.secho(f": {app.scripts_path()}")
    click.secho(f"templates_path", nl=False, fg='white')
    click.secho(f": {app.templates_path()}")
    click.echo()


@click.command()
@click.pass_context
def test(ctx: ClickContext):
    # app: App = ctx.find_root().obj
    pass
