import click


@click.command()
def desktop():
    pass


@click.command()
def lemp():
    pass


@click.command()
def mqtt():
    pass


@click.command()
def server():
    pass


@click.group()
def setup():
    pass


setup.add_command(desktop)
setup.add_command(lemp)
setup.add_command(mqtt)
setup.add_command(server)
