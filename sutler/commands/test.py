import click
from ..application import App
from ..support import OS


@click.command()
def context():
    app = App()
    app.context.print()


@click.command()
def test():
    print(f"os type:      {OS.type()}")
    print(f"os type like: {OS.type_like()}")
