import click
from ..application import App
from ..support import Version


@click.command()
def context():
    app = App()
    app.context.print()


@click.command()
def test():
    version_a = (8, 1)
    version_b = '8.1.1'
    print(f"Version({str(version_a)}) == Version({str(version_b)})")
    print(str(Version((8, 1)) == Version('8.1.0')))
    # print(Version('7.4'))
