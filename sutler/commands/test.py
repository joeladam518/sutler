import click
from click.core import Context as ClickContext
from ..application import App
from ..support import OS


@click.command()
@click.pass_context
def context(ctx: ClickContext):
    app: App = ctx.find_root().obj
    app.context.print()


@click.command()
@click.pass_context
def test(ctx: ClickContext):
    print(f"os type:      {OS.type()}")
    print(f"os type like: {OS.type_like()}")
