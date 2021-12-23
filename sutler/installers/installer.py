from click.core import Context
from abc import ABC
from ..application import App


class Installer(ABC):
    def __init__(self, ctx: Context):
        self.ctx: Context = ctx
        self.app: App = self.ctx.find_root().obj.get('app', App())
