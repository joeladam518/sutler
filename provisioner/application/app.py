import click
from jinja2 import Environment, FileSystemLoader
from .singleton import SingletonMeta
from .config import Config
from .context import Context


class App(metaclass=SingletonMeta):
    def __init__(self):
        self.config = Config()
        self.context = Context()
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.context.get_path('templates'))
        )

    def print_user(self):
        click.secho(f" uid: {self.context.get_user('uid', '')}", fg='bright_yellow')
        click.secho(f"name: {self.context.get_user('name', '')}", fg='bright_yellow')
        click.secho(f"home: {self.context.get_user('home', '')}", fg='bright_yellow')
        click.echo()
        click.secho(f"      src path: {self.context.get_path('src')}", fg='bright_cyan')
        click.secho(f"templates path: {self.context.get_path('templates')}", fg='bright_cyan')
