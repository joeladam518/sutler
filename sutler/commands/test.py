import click
from click.core import Context as ClickContext
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..application import App


@click.command()
@click.pass_context
def test(ctx: ClickContext):
    app: 'App' = ctx.find_root().obj
    app.print()
