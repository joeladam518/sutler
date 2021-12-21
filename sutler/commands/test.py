import click
from ..application import App
from ..support import Version


@click.command()
def context():
    app = App()
    app.context.print()


@click.command()
def test():
    print(str(Version((8, 1)) == Version('8.1.0')))
    # print(Version('7.4'))
