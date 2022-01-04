import click
import os
from pathlib import Path
from click.core import Context as ClickContext
from ..application import App


@click.command()
@click.pass_context
def test(ctx: ClickContext):
    app: App = ctx.find_root().obj
    app.print()
