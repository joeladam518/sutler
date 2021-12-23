from abc import ABC
from ..application import App
from click.core import Context as ClickContext


class Installer(ABC):
    def __init__(self, ctx: ClickContext):
        self.ctx: ClickContext = ctx
        self.app: App = self.ctx.find_root().obj.get('app', App())
