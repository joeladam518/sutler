from jinja2 import Environment, FileSystemLoader
from .config import Config
from .context import Context
from .singleton import SingletonMeta


class App(metaclass=SingletonMeta):
    def __init__(self, **kwargs):
        self.config = kwargs.get('config', Config())
        self.context = kwargs.get('context', Context())
        self.jinja = Environment(
            loader=FileSystemLoader(self.context.get_path('templates'))
        )

    def config(self, key: str, default=None):
        return self.config.get(key, default)

    def validate(self, type_key: str, type_: str) -> bool:
        return self.config.validate_type(type_key, type_)
